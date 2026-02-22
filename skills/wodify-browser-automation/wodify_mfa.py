#!/usr/bin/env python3
"""
Wodify Browser Automation - MFA-Aware Edition
Handles Multi-Factor Authentication via email code.

Usage:
    python3 wodify_mfa.py test-login
    python3 wodify_mfa.py list-clients
    python3 wodify_mfa.py add-client "Name" "Email" "Phone"
    python3 wodify_mfa.py extract-prices
"""

import argparse
import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("Error: playwright not installed.")
    sys.exit(1)

# Configuration
CONFIG_DIR = Path.home() / ".wodify"
CONFIG_FILE = CONFIG_DIR / "credentials.json"
SESSION_FILE = CONFIG_DIR / "session_state.json"
LOG_FILE = CONFIG_DIR / "activity.log"
WODIFY_LOGIN_URL = "https://app.wodify.com/SignIn/"
WODIFY_ADMIN_URL = "https://app.wodify.com/Admin"

def log(action: str, details: str = ""):
    """Log activity to file"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {action}: {details}\n")

def load_credentials():
    """Load credentials from config file"""
    if not CONFIG_FILE.exists():
        print(f"Error: Config file not found at {CONFIG_FILE}")
        sys.exit(1)
    
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_session_state(page):
    """Save session storage and local storage for persistence"""
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
        print("  Session state saved")
    except Exception as e:
        print(f"  Warning: Could not save session state: {e}")

def load_session_state(page):
    """Load session storage and local storage - must be called after page.goto()"""
    if not SESSION_FILE.exists():
        return False
    
    try:
        with open(SESSION_FILE) as f:
            state = json.load(f)
        
        # Check if session is recent (< 24 hours)
        saved_time = datetime.fromisoformat(state.get("timestamp", "2000-01-01"))
        if (datetime.now() - saved_time).total_seconds() > 86400:  # 24 hours
            print("  Session expired (older than 24h)")
            return False
        
        # Restore storage - must be on same domain
        session_data = state.get("session_storage", {})
        local_data = state.get("local_storage", {})
        
        if session_data or local_data:
            try:
                page.evaluate("""
                    (data) => {
                        for (const [key, value] of Object.entries(data.session)) {
                            try { sessionStorage.setItem(key, value); } catch(e) {}
                        }
                        for (const [key, value] of Object.entries(data.local)) {
                            try { localStorage.setItem(key, value); } catch(e) {}
                        }
                    }
                """, {"session": session_data, "local": local_data})
                print("  Session state restored")
            except Exception as e:
                print(f"  Warning: Could not restore storage: {e}")
        
        return True
    except Exception as e:
        print(f"  Warning: Could not load session state: {e}")
        return False

def create_browser(headless=True):
    """Create browser instance"""
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless)
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    return p, browser, context, page

def close_browser(p, browser, context, page):
    """Save session and close browser"""
    try:
        save_session_state(page)
    except Exception as e:
        pass
    try:
        browser.close()
    except:
        pass
    try:
        p.stop()
    except:
        pass

def is_logged_in(page):
    """Check if currently logged in"""
    return any(x in page.url for x in ["Home", "Dashboard", "WOD", "Admin", "Main"]) and "SignIn" not in page.url

def handle_mfa(page, creds):
    """Handle MFA/2FA flow - select email option"""
    print("  MFA Required - Selecting email authentication...")
    
    try:
        # Click on "Email a code" option
        email_option = page.wait_for_selector('text=/Email a code/', timeout=10000)
        if email_option:
            email_option.click()
            print("  Clicked 'Email a code' option")
        
        page.wait_for_timeout(2000)
        
        # Look for "Send Code" or similar button
        send_buttons = [
            'button:has-text("Send")',
            'button:has-text("Send Code")',
            'button:has-text("Continue")',
            'button[type="submit"]'
        ]
        
        for btn in send_buttons:
            try:
                page.click(btn)
                print(f"  Clicked send button: {btn}")
                break
            except:
                continue
        
        print("\n⚠️  MFA CODE SENT TO EMAIL")
        print("   Please check your email and provide the code:")
        
        # For automated runs, we can't handle MFA without email access
        # Save state and return False - user needs to complete MFA manually first
        print("\n   To fix this:")
        print("   1. Run with --show flag: python3 wodify_mfa.py test-login --show")
        print("   2. Complete MFA manually in the browser")
        print("   3. The session will be saved for future automated runs")
        
        return False
        
    except Exception as e:
        print(f"  MFA handling error: {e}")
        return False

def login(page, creds, headless=True):
    """Login to Wodify with MFA awareness"""
    print("Logging into Wodify...")
    
    # Navigate first, then try to restore session
    page.goto("https://app.wodify.com/")
    page.wait_for_timeout(2000)
    
    # Try to restore session
    has_session = load_session_state(page)
    if has_session:
        print("  Attempting to use saved session...")
        page.reload()
        page.wait_for_timeout(3000)
        
        if is_logged_in(page):
            print("✓ Session restored - already logged in")
            return True
        print("  Session invalid, logging in fresh...")
    
    # Fresh login
    page.goto(WODIFY_LOGIN_URL)
    page.wait_for_timeout(3000)
    
    if is_logged_in(page):
        print("✓ Already logged in")
        return True
    
    try:
        # Step 1: Enter email
        print("  Step 1: Email...")
        page.fill('input[type="email"]', creds["email"])
        page.click('button:has-text("CONTINUE")')
        page.wait_for_timeout(2000)
        
        # Step 2: Enter password
        print("  Step 2: Password...")
        page.wait_for_selector('input[type="password"]', timeout=10000)
        page.fill('input[type="password"]', creds["password"])
        page.click('button:has-text("Sign In")')
        
        # Wait for navigation
        page.wait_for_timeout(4000)
        
        # Check for MFA
        if "Verify" in page.title() or page.query_selector('text=/Verify your Identity/'):
            if headless:
                print("\n⚠️  MFA Required but running in headless mode")
                print("   Run with --show to complete MFA once, then session will persist")
                return False
            return handle_mfa(page, creds)
        
        # Check if logged in
        if is_logged_in(page):
            print("✓ Login successful")
            return True
        elif "SignIn" in page.url:
            print("✗ Login failed - still on login page")
            return False
        else:
            print(f"? Unexpected page: {page.url}")
            return False
            
    except Exception as e:
        print(f"✗ Login error: {e}")
        return False

def extract_membership_prices(page):
    """Extract membership pricing from Wodify"""
    print("\nExtracting membership prices...")
    
    prices = {}
    
    try:
        # Navigate to memberships page
        print("  Navigating to memberships...")
        page.goto(f"{WODIFY_ADMIN_URL}/Memberships")
        page.wait_for_timeout(5000)
        
        # Take screenshot for debugging
        OUTPUT_DIR = Path("/Users/daneel/.openclaw/workspace/skills/wodify-browser-automation/agent-task")
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(OUTPUT_DIR / "memberships-page.png"))
        
        # Try to find price information
        # Common locations: membership cards, pricing tables, subscription lists
        
        # Look for dollar amounts in the page
        content = page.content()
        price_matches = re.findall(r'\$[\d,]+(?:\.\d{2})?', content)
        if price_matches:
            print(f"  Found prices: {list(set(price_matches))}")
            prices["all_prices"] = list(set(price_matches))
        
        # Look for membership rows
        rows = page.query_selector_all('table tr, .membership-row, [data-membership]')
        memberships = []
        
        for row in rows:
            try:
                name_elem = row.query_selector('td:nth-child(1), .membership-name')
                price_elem = row.query_selector('td:nth-child(2), .membership-price, .price')
                
                if name_elem and price_elem:
                    name = name_elem.inner_text().strip()
                    price = price_elem.inner_text().strip()
                    if name and price:
                        memberships.append({"name": name, "price": price})
            except:
                continue
        
        if memberships:
            print(f"  Found {len(memberships)} memberships:")
            for m in memberships:
                print(f"    • {m['name']}: {m['price']}")
            prices["memberships"] = memberships
        
        # Save results
        results_file = OUTPUT_DIR / "membership-prices.json"
        with open(results_file, "w") as f:
            json.dump(prices, f, indent=2)
        print(f"\n  Results saved to: {results_file}")
        
        return prices
        
    except Exception as e:
        print(f"✗ Error extracting prices: {e}")
        return {}

def list_clients(page):
    """List all active clients"""
    print("Listing clients...")
    log("LIST_CLIENTS")
    
    try:
        page.goto(f"{WODIFY_ADMIN_URL}/Clients")
        page.wait_for_timeout(4000)
        
        clients = []
        rows = page.query_selector_all('table tr, .client-row, [data-client]')
        
        for row in rows:
            try:
                name_elem = row.query_selector('td:nth-child(1), .client-name')
                email_elem = row.query_selector('td:nth-child(2), .client-email')
                status_elem = row.query_selector('td:nth-child(3), .client-status')
                
                if name_elem:
                    clients.append({
                        "name": name_elem.inner_text().strip(),
                        "email": email_elem.inner_text().strip() if email_elem else "",
                        "status": status_elem.inner_text().strip() if status_elem else ""
                    })
            except:
                continue
        
        print(f"\nFound {len(clients)} clients:")
        for c in clients[:20]:
            print(f"  • {c['name']} | {c['email']} | {c['status']}")
        
        return clients
    except Exception as e:
        print(f"Error listing clients: {e}")
        return []

def add_client(page, name: str, email: str, phone: str):
    """Add a new client"""
    print(f"Adding client: {name}")
    log("ADD_CLIENT", f"{name} | {email} | {phone}")
    
    try:
        page.goto(f"{WODIFY_ADMIN_URL}/Clients")
        page.wait_for_timeout(3000)
        
        # Click Add New Client
        page.click('button:has-text("New"), button:has-text("Add"), a:has-text("Add Client")')
        page.wait_for_timeout(2000)
        
        # Fill in details
        first_name = name.split()[0]
        last_name = " ".join(name.split()[1:]) if len(name.split()) > 1 else ""
        
        page.fill('input[name*="First"], input[placeholder*="First"]', first_name)
        if last_name:
            page.fill('input[name*="Last"], input[placeholder*="Last"]', last_name)
        page.fill('input[name*="Email"], input[type="email"]', email)
        page.fill('input[name*="Phone"], input[type="tel"]', phone)
        
        # Save
        page.click('button:has-text("Save"), button:has-text("Create")')
        page.wait_for_timeout(2000)
        
        print(f"✓ Client '{name}' added successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to add client: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Wodify Admin Automation (MFA-Aware)")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Test login
    test_parser = subparsers.add_parser("test-login", help="Test login only")
    test_parser.add_argument("--show", action="store_true", help="Show browser window")
    
    # Extract prices
    price_parser = subparsers.add_parser("extract-prices", help="Extract membership prices")
    price_parser.add_argument("--show", action="store_true", help="Show browser window")
    
    # Add client
    add_parser = subparsers.add_parser("add-client", help="Add a new client")
    add_parser.add_argument("--show", action="store_true", help="Show browser window")
    add_parser.add_argument("name", help="Client full name")
    add_parser.add_argument("email", help="Client email")
    add_parser.add_argument("phone", help="Client phone")
    
    # List clients
    list_parser = subparsers.add_parser("list-clients", help="List all active clients")
    list_parser.add_argument("--show", action="store_true", help="Show browser window")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Load credentials
    creds = load_credentials()
    
    # Create browser
    p, browser, context, page = create_browser(headless=not args.show)
    
    try:
        # Login
        if not login(page, creds, headless=not args.show):
            print("\n❌ Login failed")
            close_browser(p, browser, context, page)
            sys.exit(1)
        
        # Execute command
        if args.command == "test-login":
            print("\n✓ Login test passed")
        elif args.command == "extract-prices":
            prices = extract_membership_prices(page)
            print(f"\nExtracted {len(prices)} price entries")
        elif args.command == "list-clients":
            list_clients(page)
        elif args.command == "add-client":
            add_client(page, args.name, args.email, args.phone)
        
    finally:
        close_browser(p, browser, context, page)

if __name__ == "__main__":
    main()
