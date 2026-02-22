#!/usr/bin/env python3
"""Debug Wodify login - capture screenshots and HTML for diagnosis"""

import json
import sys
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: playwright not installed.")
    sys.exit(1)

CONFIG_DIR = Path.home() / ".wodify"
CONFIG_FILE = CONFIG_DIR / "credentials.json"
OUTPUT_DIR = Path("/Users/daneel/.openclaw/workspace/skills/wodify-browser-automation/agent-task")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_credentials():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_screenshot(page, name):
    ts = datetime.now().strftime("%H%M%S")
    path = OUTPUT_DIR / f"debug-{name}-{ts}.png"
    page.screenshot(path=str(path), full_page=True)
    print(f"  Screenshot saved: {path}")
    return path

def save_html(page, name):
    ts = datetime.now().strftime("%H%M%S")
    path = OUTPUT_DIR / f"debug-{name}-{ts}.html"
    path.write_text(page.content())
    print(f"  HTML saved: {path}")
    return path

def main():
    creds = load_credentials()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser
        context = browser.new_context()
        page = context.new_page()
        
        print("Navigating to login page...")
        page.goto("https://app.wodify.com/SignIn/")
        page.wait_for_timeout(2000)
        
        save_screenshot(page, "01-initial")
        save_html(page, "01-initial")
        
        print("\nCurrent URL:", page.url)
        print("Page title:", page.title())
        
        # Check what input fields exist
        print("\n--- Input fields on page ---")
        inputs = page.query_selector_all('input')
        for i, inp in enumerate(inputs):
            itype = inp.get_attribute('type') or 'text'
            name = inp.get_attribute('name') or ''
            placeholder = inp.get_attribute('placeholder') or ''
            print(f"  {i}: type={itype}, name={name}, placeholder={placeholder}")
        
        # Check for buttons
        print("\n--- Buttons on page ---")
        buttons = page.query_selector_all('button')
        for i, btn in enumerate(buttons):
            text = btn.inner_text().strip() if btn else ''
            btype = btn.get_attribute('type') or ''
            print(f"  {i}: text='{text}', type={btype}")
        
        # Step 1: Email
        print("\nStep 1: Entering email...")
        email_selectors = [
            'input[type="email"]',
            'input[name*="Email" i]',
            'input[placeholder*="Email" i]',
            'input#Email',
            'input#email'
        ]
        
        email_field = None
        for sel in email_selectors:
            try:
                email_field = page.wait_for_selector(sel, timeout=2000)
                if email_field:
                    print(f"  Found email field: {sel}")
                    break
            except:
                continue
        
        if email_field:
            email_field.fill(creds["email"])
            print(f"  Filled email: {creds['email'][:3]}...")
        else:
            print("  ERROR: Could not find email field!")
            save_screenshot(page, "error-no-email")
            browser.close()
            return
        
        save_screenshot(page, "02-email-filled")
        
        # Click Continue
        print("\nClicking CONTINUE...")
        continue_selectors = [
            'button:has-text("CONTINUE")',
            'button:has-text("Continue")',
            'button[type="submit"]'
        ]
        
        for sel in continue_selectors:
            try:
                page.click(sel)
                print(f"  Clicked: {sel}")
                break
            except:
                continue
        
        page.wait_for_timeout(3000)
        save_screenshot(page, "03-after-continue")
        save_html(page, "03-after-continue")
        
        print(f"\nURL after continue: {page.url}")
        
        # Step 2: Password
        print("\nStep 2: Entering password...")
        password_selectors = [
            'input[type="password"]',
            'input[name*="Password" i]',
            'input#Password',
            'input#password'
        ]
        
        password_field = None
        for sel in password_selectors:
            try:
                password_field = page.wait_for_selector(sel, timeout=5000)
                if password_field:
                    print(f"  Found password field: {sel}")
                    break
            except:
                continue
        
        if password_field:
            password_field.fill(creds["password"])
            print("  Filled password: ***")
        else:
            print("  ERROR: Could not find password field!")
            print("  Checking page for password input...")
            inputs = page.query_selector_all('input')
            for inp in inputs:
                itype = inp.get_attribute('type') or 'text'
                print(f"    Input type: {itype}")
            save_screenshot(page, "error-no-password")
            browser.close()
            return
        
        save_screenshot(page, "04-password-filled")
        
        # Click Sign In
        print("\nClicking Sign In...")
        signin_selectors = [
            'button:has-text("Sign In")',
            'button:has-text("SIGN IN")',
            'button:has-text("Login")',
            'button[type="submit"]'
        ]
        
        for sel in signin_selectors:
            try:
                page.click(sel)
                print(f"  Clicked: {sel}")
                break
            except:
                continue
        
        page.wait_for_timeout(5000)
        save_screenshot(page, "05-after-signin")
        save_html(page, "05-after-signin")
        
        print(f"\nFinal URL: {page.url}")
        print(f"Page title: {page.title()}")
        
        if "SignIn" in page.url:
            print("\n❌ LOGIN FAILED - Still on sign in page")
            # Check for error messages
            errors = page.query_selector_all('.error, .alert, [role="alert"]')
            for err in errors:
                print(f"  Error: {err.inner_text()}")
        else:
            print("\n✅ LOGIN SUCCESS")
        
        browser.close()

if __name__ == "__main__":
    main()
