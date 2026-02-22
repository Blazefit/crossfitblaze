#!/usr/bin/env python3
"""
Wodify MFA Setup Script - Complete MFA once to save session
Run this in visible mode to complete MFA, then automation will work.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import time

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: playwright not installed.")
    sys.exit(1)

CONFIG_DIR = Path.home() / ".wodify"
CONFIG_FILE = CONFIG_DIR / "credentials.json"
SESSION_FILE = CONFIG_DIR / "session_state.json"

def load_credentials():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_session(page):
    """Save session storage and cookies"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        session_storage = page.evaluate("() => JSON.stringify(sessionStorage)")
        local_storage = page.evaluate("() => JSON.stringify(localStorage)")
        
        state = {
            "url": page.url,
            "session_storage": json.loads(session_storage) if session_storage else {},
            "local_storage": json.loads(local_storage) if local_storage else {},
            "timestamp": datetime.now().isoformat()
        }
        
        with open(SESSION_FILE, "w") as f:
            json.dump(state, f)
        print("\n✓ Session saved successfully!")
        print(f"  Location: {SESSION_FILE}")
        return True
    except Exception as e:
        print(f"  Error saving session: {e}")
        return False

def main():
    creds = load_credentials()
    
    print("=" * 60)
    print("Wodify MFA Setup")
    print("=" * 60)
    print("\nThis script will help you complete MFA once.")
    print("After that, automated runs will use the saved session.\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        
        print("Opening Wodify login page...")
        page.goto("https://app.wodify.com/SignIn/")
        page.wait_for_timeout(2000)
        
        # Enter email
        print("Entering email...")
        page.fill('input[type="email"]', creds["email"])
        page.click('button:has-text("CONTINUE")')
        page.wait_for_timeout(2000)
        
        # Enter password
        print("Entering password...")
        page.fill('input[type="password"]', creds["password"])
        page.click('button:has-text("Sign In")')
        page.wait_for_timeout(3000)
        
        # Check if we hit MFA
        page_title = page.title()
        if "Verify" in page_title or page.query_selector('text=/Verify your Identity/'):
            print("\n" + "=" * 60)
            print("MFA REQUIRED - ACTION NEEDED")
            print("=" * 60)
            print("\n1. Click 'Email a code' in the browser")
            print("2. Check your email for the code")
            print("3. Enter the code in the browser")
            print("4. Press ENTER here when you've completed MFA")
            print("=" * 60)
            input("\nPress ENTER after completing MFA in the browser...")
        
        # Check if we're logged in
        page.wait_for_timeout(3000)
        current_url = page.url
        
        if "SignIn" not in current_url:
            print("\n✓ Login appears successful!")
            print(f"  Current URL: {current_url}")
            save_session(page)
            print("\nFuture automated runs will use this session.")
        else:
            print("\n✗ Still on login page - MFA may not be complete")
            
        browser.close()

if __name__ == "__main__":
    main()
