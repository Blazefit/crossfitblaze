#!/usr/bin/env python3
"""
Wodify Browser Automation - Manage gym members via browser automation
No API required - uses Playwright to automate the Wodify admin interface.

Usage:
    python3 wodify.py add-client "Name" "Email" "Phone"
    python3 wodify.py list-clients
    python3 wodify.py search "Name"
    python3 wodify.py hold-client "Name" "Reason"
    python3 wodify.py remove-client "Name"
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("Error: playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

# Configuration
CONFIG_DIR = Path.home() / ".wodify"
CONFIG_FILE = CONFIG_DIR / "credentials.json"
COOKIES_FILE = CONFIG_DIR / "cookies.json"
LOG_FILE = CONFIG_DIR / "activity.log"
WODIFY_LOGIN_URL = "https://app.wodify.com/Security/Login"
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
        print(f"Create it from config.template.json")
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

def login(page, creds):
    """Login to Wodify"""
    print("Logging into Wodify...")
    
    page.goto(WODIFY_LOGIN_URL)
    page.wait_for_load_state("networkidle")
    
    # Check if already logged in
    if "Admin" in page.url or "Dashboard" in page.url:
        print("Already logged in (session restored)")
        return True
    
    # Fill login form
    try:
        page.fill('input[name="Username"], input[type="email"], #Username', creds["email"])
        page.fill('input[name="Password"], input[type="password"], #Password', creds["password"])
        page.click('button[type="submit"], input[type="submit"], .login-button')
        
        # Wait for login to complete
        page.wait_for_url("**/Admin**", timeout=15000)
        print("Login successful")
        return True
    except PlaywrightTimeout:
        print("Login failed - check credentials")
        return False
    except Exception as e:
        print(f"Login error: {e}")
        return False

def create_browser(headless=True):
    """Create browser instance"""
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless)
    context = browser.new_context()
    
    # Try to load existing cookies
    has_session = load_cookies(context)
    
    page = context.new_page()
    return p, browser, context, page, has_session

def close_browser(p, browser, context):
    """Save cookies and close browser"""
    save_cookies(context)
    browser.close()
    p.stop()

def add_client(page, name: str, email: str, phone: str):
    """Add a new client"""
    print(f"Adding client: {name}")
    log("ADD_CLIENT", f"{name} | {email} | {phone}")
    
    # Navigate to clients/members section
    page.goto(f"{WODIFY_ADMIN_URL}/Clients")
    page.wait_for_load_state("networkidle")
    
    try:
        # Click Add New Client button
        page.click('button:has-text("Add"), a:has-text("Add Client"), .add-client-btn')
        page.wait_for_load_state("networkidle")
        
        # Fill in client details
        page.fill('input[name="FirstName"], #FirstName', name.split()[0])
        if len(name.split()) > 1:
            page.fill('input[name="LastName"], #LastName', ' '.join(name.split()[1:]))
        page.fill('input[name="Email"], #Email', email)
        page.fill('input[name="Phone"], #Phone', phone)
        
        # Save
        page.click('button:has-text("Save"), button:has-text("Add"), input[type="submit"]')
        page.wait_for_load_state("networkidle")
        
        print(f"✓ Client '{name}' added successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to add client: {e}")
        return False

def list_clients(page):
    """List all active clients"""
    print("Listing clients...")
    log("LIST_CLIENTS")
    
    page.goto(f"{WODIFY_ADMIN_URL}/Clients")
    page.wait_for_load_state("networkidle")
    
    clients = []
    try:
        # Get client rows from table
        rows = page.query_selector_all('table tbody tr, .client-list .client-item')
        
        for row in rows:
            try:
                name = row.query_selector('td:nth-child(1), .client-name').inner_text()
                email = row.query_selector('td:nth-child(2), .client-email').inner_text()
                status = row.query_selector('td:nth-child(3), .client-status').inner_text()
                clients.append({"name": name.strip(), "email": email.strip(), "status": status.strip()})
            except:
                continue
        
        print(f"\nFound {len(clients)} clients:\n")
        for c in clients:
            print(f"  • {c['name']} | {c['email']} | {c['status']}")
        
        return clients
    except Exception as e:
        print(f"Error listing clients: {e}")
        return []

def search_client(page, query: str):
    """Search for a client"""
    print(f"Searching for: {query}")
    log("SEARCH_CLIENT", query)
    
    page.goto(f"{WODIFY_ADMIN_URL}/Clients")
    page.wait_for_load_state("networkidle")
    
    try:
        # Use search box
        page.fill('input[type="search"], input[name="search"], .search-input', query)
        page.press('input[type="search"], input[name="search"], .search-input', 'Enter')
        page.wait_for_load_state("networkidle")
        
        # Get results
        rows = page.query_selector_all('table tbody tr, .client-list .client-item')
        results = []
        
        for row in rows:
            try:
                name = row.query_selector('td:nth-child(1), .client-name').inner_text()
                if query.lower() in name.lower():
                    email = row.query_selector('td:nth-child(2), .client-email').inner_text()
                    results.append({"name": name.strip(), "email": email.strip()})
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
    
    # Search for client first
    results = search_client(page, name)
    
    if not results:
        print(f"✗ Client '{name}' not found")
        return False
    
    try:
        # Click on client to open details
        page.click(f'text="{name}"')
        page.wait_for_load_state("networkidle")
        
        # Find and click Hold button
        page.click('button:has-text("Hold"), a:has-text("Put on Hold")')
        
        # Enter reason
        page.fill('textarea[name="Reason"], input[name="Reason"], #HoldReason', reason)
        
        # Confirm
        page.click('button:has-text("Confirm"), button:has-text("Save")')
        page.wait_for_load_state("networkidle")
        
        print(f"✓ Client '{name}' placed on hold")
        return True
    except Exception as e:
        print(f"✗ Failed to hold client: {e}")
        return False

def remove_client(page, name: str):
    """Remove/cancel a client"""
    print(f"Removing client: {name}")
    log("REMOVE_CLIENT", name)
    
    # Search for client first
    results = search_client(page, name)
    
    if not results:
        print(f"✗ Client '{name}' not found")
        return False
    
    try:
        # Click on client to open details
        page.click(f'text="{name}"')
        page.wait_for_load_state("networkidle")
        
        # Find and click Delete/Cancel button
        page.click('button:has-text("Delete"), button:has-text("Cancel"), a:has-text("Remove")')
        
        # Confirm deletion
        page.click('button:has-text("Confirm"), button:has-text("Yes")')
        page.wait_for_load_state("networkidle")
        
        print(f"✓ Client '{name}' removed")
        return True
    except Exception as e:
        print(f"✗ Failed to remove client: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Wodify Browser Automation")
    parser.add_argument("--show", action="store_true", help="Show browser window")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add client
    add_parser = subparsers.add_parser("add-client", help="Add a new client")
    add_parser.add_argument("name", help="Client name")
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
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Load credentials
    creds = load_credentials()
    
    # Create browser
    p, browser, context, page, has_session = create_browser(headless=not args.show)
    
    try:
        # Login if needed
        if not has_session:
            if not login(page, creds):
                sys.exit(1)
        else:
            # Verify session is still valid
            page.goto(WODIFY_ADMIN_URL)
            if "Login" in page.url:
                if not login(page, creds):
                    sys.exit(1)
        
        # Execute command
        if args.command == "add-client":
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
