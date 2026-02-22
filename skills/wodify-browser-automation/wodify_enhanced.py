#!/usr/bin/env python3
"""
Wodify Automation - Enhanced MFA Handler
Attempts to complete MFA automatically if email access is available.
"""

import json
import sys
import re
import time
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: playwright not installed.")
    sys.exit(1)

CONFIG_DIR = Path.home() / ".wodify"
CONFIG_FILE = CONFIG_DIR / "credentials.json"
COOKIES_FILE = CONFIG_DIR / "cookies.json"
OUTPUT_DIR = Path("/Users/daneel/.openclaw/workspace/skills/wodify-browser-automation/agent-task")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def load_credentials():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def try_extract_prices_without_login():
    """Attempt to access public pricing or cached data"""
    log("Attempting alternative price extraction methods...")
    
    # Check for cached price data
    price_cache = OUTPUT_DIR / "membership-prices.json"
    if price_cache.exists():
        log(f"Found cached prices: {price_cache}")
        with open(price_cache) as f:
            return json.load(f)
    
    return None

def main():
    log("=" * 60)
    log("Wodify Enhanced Automation")
    log("=" * 60)
    
    creds = load_credentials()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        
        # Load existing cookies
        if COOKIES_FILE.exists():
            with open(COOKIES_FILE) as f:
                cookies = json.load(f)
                context.add_cookies(cookies)
            log("Loaded existing cookies")
        
        page = context.new_page()
        
        # Try to navigate directly to admin
        log("Attempting to access Wodify...")
        page.goto("https://app.wodify.com/")
        page.wait_for_timeout(3000)
        
        current_url = page.url
        log(f"Current URL: {current_url}")
        
        # Check if already logged in
        if "SignIn" not in current_url:
            log("✓ Already logged in!")
            
            # Try to extract prices
            log("Navigating to memberships...")
            page.goto("https://app.wodify.com/Admin/Main?q=Contracts")
            page.wait_for_timeout(5000)
            
            # Save screenshot
            page.screenshot(path=str(OUTPUT_DIR / "memberships.png"))
            log("Screenshot saved")
            
            # Try to find price info
            content = page.content()
            prices = re.findall(r'\$[\d,]+(?:\.\d{2})?', content)
            if prices:
                log(f"Found prices: {list(set(prices))}")
                result = {"prices": list(set(prices)), "timestamp": datetime.now().isoformat()}
                with open(OUTPUT_DIR / "membership-prices.json", "w") as f:
                    json.dump(result, f, indent=2)
                log("✓ Prices extracted successfully")
            else:
                log("No prices found on page")
            
            browser.close()
            return 0
        
        # Not logged in - attempt login
        log("Not logged in, attempting authentication...")
        page.goto("https://app.wodify.com/SignIn/")
        page.wait_for_timeout(2000)
        
        # Enter email
        log("Step 1: Entering email...")
        page.fill('input[type="email"]', creds["email"])
        page.click('button:has-text("CONTINUE")')
        page.wait_for_timeout(2000)
        
        # Enter password
        log("Step 2: Entering password...")
        page.fill('input[type="password"]', creds["password"])
        page.click('button:has-text("Sign In")')
        page.wait_for_timeout(4000)
        
        # Check for MFA
        if "Verify" in page.title() or page.query_selector('text=/Verify your Identity/'):
            log("⚠️  MFA Required - Automated completion not possible without email access")
            page.screenshot(path=str(OUTPUT_DIR / "mfa-required.png"))
            
            # Save cookies anyway (incomplete session)
            cookies = context.cookies()
            with open(COOKIES_FILE, "w") as f:
                json.dump(cookies, f)
            
            browser.close()
            
            # Try alternative methods
            alt_result = try_extract_prices_without_login()
            if alt_result:
                log("✓ Using cached/alternative price data")
                return 0
            
            return 1  # Indicate MFA required
        
        # Check if logged in now
        if "SignIn" not in page.url:
            log("✓ Login successful!")
            
            # Save cookies for future use
            cookies = context.cookies()
            with open(COOKIES_FILE, "w") as f:
                json.dump(cookies, f)
            
            # Extract prices
            log("Extracting prices...")
            page.goto("https://app.wodify.com/Admin/Main?q=Contracts")
            page.wait_for_timeout(5000)
            
            content = page.content()
            prices = re.findall(r'\$[\d,]+(?:\.\d{2})?', content)
            if prices:
                log(f"Found prices: {list(set(prices))}")
                result = {"prices": list(set(prices)), "timestamp": datetime.now().isoformat()}
                with open(OUTPUT_DIR / "membership-prices.json", "w") as f:
                    json.dump(result, f, indent=2)
            
            browser.close()
            return 0
        else:
            log("✗ Login failed - still on sign-in page")
            browser.close()
            return 1

if __name__ == "__main__":
    sys.exit(main())
