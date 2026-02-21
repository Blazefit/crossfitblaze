#!/Users/daneel/.openclaw/workspace/skills/wodify-browser-automation/venv/bin/python3
"""
Wodify Browser Automation - Admin Edition (Kimi 2.5)
Works with admin-level Wodify access for client management.

Usage:
    python3 wodify.py add-client "Name" "Email" "Phone"
    python3 wodify.py list-clients
    python3 wodify.py hold-client "Name" "Reason"
    python3 wodify.py remove-client "Name"
"""

import argparse
import json
import os
import sys
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
COOKIES_FILE = CONFIG_DIR / "cookies.json"
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
        print("Create it with: echo '{\"email\":\"your@email.com\",\"password\":\"yourpass\"}' > ~/.wodify/credentials.json")
        sys.exit(1)
    
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_cookies(context):
    """Save browser cookies for session persistence"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    cookies = context.cookies()
    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies, f)

def load_cookies(context):
    """Load saved cookies if they exist"""
    if COOKIES_FILE.exists():
        with open(COOKIES_FILE) as f:
            cookies = json.load(f)
            context.add_cookies(cookies)
            return True
    return False

def create_browser(headless=True):
    """Create browser instance"""
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless)
    context = browser.new_context()
    has_session = load_cookies(context)
    page = context.new_page()
    return p, browser, context, page, has_session

def close_browser(p, browser, context):
    """Save cookies and close browser"""
    save_cookies(context)
    browser.close()
    p.stop()

def login(page, creds):
    """Login to Wodify - Two step process"""
    print("Logging into Wodify...")
    
    page.goto(WODIFY_LOGIN_URL)
    page.wait_for_timeout(2000)
    
    # Check if already logged in
    if any(x in page.url for x in ["Home", "Dashboard", "WOD", "Admin", "Main"]):
        print("Already logged in (session restored)")
        return True
    
    try:
        # Step 1: Enter email
        print("  Step 1: Email...")
        page.fill('input[placeholder*="Email"], input[type="email"]', creds["email"])
        page.click('button:has-text("CONTINUE")')
        page.wait_for_timeout(2000)
        
        # Step 2: Enter password
        print("  Step 2: Password...")
        page.wait_for_selector('input[type="password"]', timeout=10000)
        page.fill('input[type="password"]', creds["password"])
        page.click('button:has-text("Sign In"), button[type="submit"]')
        
        # Wait for successful navigation
        page.wait_for_timeout(3000)
        if "SignIn" in page.url:
            print("✗ Login failed - still on login page")
            return False
        
        print("✓ Login successful")
        return True
    except Exception as e:
        print(f"✗ Login error: {e}")
        return False

def add_client(page, name: str, email: str, phone: str):
    """Add a new client"""
    print(f"Adding client: {name}")
    log("ADD_CLIENT", f"{name} | {email} | {phone}")
    
    try:
        # Navigate to clients page
        page.goto(f"{WODIFY_ADMIN_URL}/Clients")
        page.wait_for_timeout(3000)
        
        # Click Add New Client button (look for common selectors)
        page.click('button:has-text("New"), button:has-text("Add"), a:has-text("Add Client"), [data-action="add-client"]')
        page.wait_for_timeout(2000)
        
        # Fill in client details
        first_name = name.split()[0]
        last_name = " ".join(name.split()[1:]) if len(name.split()) > 1 else ""
        
        page.fill('input[name*="First"], input[placeholder*="First"]', first_name)
        if last_name:
            page.fill('input[name*="Last"], input[placeholder*="Last"]', last_name)
        page.fill('input[name*="Email"], input[type="email"]', email)
        page.fill('input[name*="Phone"], input[type="tel"]', phone)
        
        # Save
        page.click('button:has-text("Save"), button:has-text("Create"), button[type="submit"]')
        page.wait_for_timeout(2000)
        
        print(f"✓ Client '{name}' added successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to add client: {e}")
        return False

def list_clients(page):
    """List all active clients"""
    print("Listing clients...")
    log("LIST_CLIENTS")
    
    try:
        # Navigate to clients page
        page.goto(f"{WODIFY_ADMIN_URL}/Clients")
        page.wait_for_timeout(3000)
        
        # Extract client data
        clients = []
        rows = page.query_selector_all('table tr, .client-row, [data-client]')
        
        for row in rows:
            try:
                name_elem = row.query_selector('td:nth-child(1), .client-name, [data-field="name"]')
                email_elem = row.query_selector('td:nth-child(2), .client-email, [data-field="email"]')
                status_elem = row.query_selector('td:nth-child(3), .client-status, [data-field="status"]')
                
                if name_elem:
                    clients.append({
                        "name": name_elem.inner_text().strip(),
                        "email": email_elem.inner_text().strip() if email_elem else "",
                        "status": status_elem.inner_text().strip() if status_elem else ""
                    })
            except:
                continue
        
        print(f"\nFound {len(clients)} clients:\n")
        for c in clients[:20]:  # Show first 20
            print(f"  • {c['name']} | {c['email']} | {c['status']}")
        
        return clients
    except Exception as e:
        print(f"Error listing clients: {e}")
        return []

def search_client(page, query: str):
    """Search for a client"""
    print(f"Searching for: {query}")
    log("SEARCH_CLIENT", query)
    
    try:
        page.goto(f"{WODIFY_ADMIN_URL}/Clients")
        page.wait_for_timeout(3000)
        
        # Use search box
        search_box = page.query_selector('input[type="search"], input[placeholder*="Search"], .search-input')
        if search_box:
            search_box.fill(query)
            search_box.press('Enter')
            page.wait_for_timeout(2000)
        
        # Get results
        results = []
        rows = page.query_selector_all('table tr, .client-row')
        
        for row in rows:
            try:
                name_elem = row.query_selector('td:nth-child(1), .client-name')
                if name_elem and query.lower() in name_elem.inner_text().lower():
                    email_elem = row.query_selector('td:nth-child(2), .client-email')
                    results.append({
                        "name": name_elem.inner_text().strip(),
                        "email": email_elem.inner_text().strip() if email_elem else ""
                    })
            except:
                continue
        
        print(f"\nFound {len(results)} matching clients:\n")
        for r in results:
            print(f"  • {r['name']} | {r['email']}")
        
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return []

def hold_client(page, name: str, reason: str):
    """Put a client on hold"""
    print(f"Putting '{name}' on hold: {reason}")
    log("HOLD_CLIENT", f"{name} | {reason}")
    
    try:
        # Find client first
        search_client(page, name)
        
        # Click on client
        page.click(f'text="{name}"')
        page.wait_for_timeout(2000)
        
        # Click Hold/Manage button
        page.click('button:has-text("Hold"), button:has-text("Manage"), a:has-text("On Hold")')
        page.wait_for_timeout(1000)
        
        # Enter reason
        reason_box = page.query_selector('textarea, input[name="reason"]')
        if reason_box:
            reason_box.fill(reason)
        
        # Confirm
        page.click('button:has-text("Confirm"), button:has-text("Save")')
        page.wait_for_timeout(2000)
        
        print(f"✓ Client '{name}' placed on hold")
        return True
    except Exception as e:
        print(f"✗ Failed to hold client: {e}")
        return False

def remove_client(page, name: str):
    """Remove/cancel a client"""
    print(f"Removing client: {name}")
    log("REMOVE_CLIENT", name)
    
    try:
        # Find client
        search_client(page, name)
        
        # Click on client
        page.click(f'text="{name}"')
        page.wait_for_timeout(2000)
        
        # Click Remove/Delete
        page.click('button:has-text("Remove"), button:has-text("Delete"), button:has-text("Cancel")')
        page.wait_for_timeout(1000)
        
        # Confirm
        page.click('button:has-text("Confirm"), button:has-text("Yes")')
        page.wait_for_timeout(2000)
        
        print(f"✓ Client '{name}' removed")
        return True
    except Exception as e:
        print(f"✗ Failed to remove client: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Wodify Admin Automation")
    parser.add_argument("--show", action="store_true", help="Show browser window")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add client
    add_parser = subparsers.add_parser("add-client", help="Add a new client")
    add_parser.add_argument("name", help="Client full name")
    add_parser.add_argument("email", help="Client email")
    add_parser.add_argument("phone", help="Client phone")
    
    # List clients
    subparsers.add_parser("list-clients", help="List all active clients")
    
    # Search
    search_parser = subparsers.add_parser("search", help="Search for a client")
    search_parser.add_argument("query", help="Search query")
    
    # Hold client
    hold_parser = subparsers.add_parser("hold-client", help="Put a client on hold")
    hold_parser.add_argument("name", help="Client name")
    hold_parser.add_argument("reason", help="Reason for hold")
    
    # Remove client
    remove_parser = subparsers.add_parser("remove-client", help="Remove a client")
    remove_parser.add_argument("name", help="Client name")
    
    # Test login
    subparsers.add_parser("test-login", help="Test login only")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Load credentials
    creds = load_credentials()
    
    # Create browser
    p, browser, context, page, has_session = create_browser(headless=not args.show)
    
    try:
        # Login
        if not login(page, creds):
            sys.exit(1)
        
        # Execute command
        if args.command == "test-login":
            print("\n✓ Login test passed")
        elif args.command == "add-client":
            add_client(page, args.name, args.email, args.phone)
        elif args.command == "list-clients":
            list_clients(page)
        elif args.command == "search":
            search_client(page, args.query)
        elif args.command == "hold-client":
            hold_client(page, args.name, args.reason)
        elif args.command == "remove-client":
            remove_client(page, args.name)
        
    finally:
        close_browser(p, browser, context)

if __name__ == "__main__":
    main()
