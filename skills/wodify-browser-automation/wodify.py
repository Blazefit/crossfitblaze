#!/Users/daneel/.openclaw/workspace/skills/wodify-browser-automation/venv/bin/python3
"""
Wodify Browser Automation - Member Edition
Works with member-level Wodify access (not admin).

Usage:
    python3 wodify.py checkin "5:30 PM WOD"
    python3 wodify.py log-workout "Fran" "4:32"
    python3 wodify.py view-schedule
    python3 wodify.py view-history
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
    print("Run: cd ~/.openclaw/workspace/skills/wodify-browser-automation && source venv/bin/activate && pip install playwright && playwright install chromium")
    sys.exit(1)

# Configuration
CONFIG_DIR = Path.home() / ".wodify"
CONFIG_FILE = CONFIG_DIR / "credentials.json"
COOKIES_FILE = CONFIG_DIR / "cookies.json"
LOG_FILE = CONFIG_DIR / "activity.log"
WODIFY_LOGIN_URL = "https://app.wodify.com/SignIn/"
WODIFY_BASE_URL = "https://app.wodify.com"

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
    page.wait_for_timeout(2000)  # Wait for page to settle
    
    # Check if already logged in
    if any(x in page.url for x in ["Home", "Dashboard", "WOD", "Admin", "Main"]):
        print("Already logged in (session restored)")
        return True
    
    try:
        # Step 1: Enter email
        print("  Step 1: Email...")
        page.fill('input[placeholder*="Email"], input[type="email"]', creds["email"])
        page.click('button:has-text("CONTINUE")')
        page.wait_for_load_state("networkidle")
        
        # Step 2: Enter password
        print("  Step 2: Password...")
        page.wait_for_selector('input[type="password"]', timeout=10000)
        page.fill('input[type="password"]', creds["password"])
        page.click('button:has-text("Sign In"), button[type="submit"]')
        
        # Wait for successful login (any destination except login page)
        page.wait_for_timeout(3000)  # Give page time to settle
        if "SignIn" in page.url:
            print("✗ Still on login page")
            return False
        print("✓ Login successful")
        return True
    except Exception as e:
        print(f"✗ Login failed: {e}")
        return False

def checkin_wod(page, wod_name: str):
    """Check into a WOD/class"""
    print(f"Checking into: {wod_name}")
    log("CHECKIN", wod_name)
    
    try:
        # Navigate to schedule/reserve page
        page.goto(f"{WODIFY_BASE_URL}/Schedule")
        page.wait_for_load_state("networkidle")
        
        # Look for the WOD and click Reserve
        # This is simplified - actual selectors depend on Wodify's UI
        page.click(f'text="{wod_name}"')
        page.click('button:has-text("Reserve"), button:has-text("Sign In")')
        
        print(f"✓ Checked into {wod_name}")
        return True
    except Exception as e:
        print(f"✗ Check-in failed: {e}")
        return False

def log_workout(page, workout_name: str, result: str):
    """Log a workout result"""
    print(f"Logging workout: {workout_name} = {result}")
    log("LOG_WORKOUT", f"{workout_name}: {result}")
    
    try:
        # Navigate to workout tracking
        page.goto(f"{WODIFY_BASE_URL}/Tracking")
        page.wait_for_load_state("networkidle")
        
        # Find workout and log result
        page.fill('input[placeholder*="Search"]', workout_name)
        page.press('input[placeholder*="Search"]', 'Enter')
        page.click(f'text="{workout_name}"')
        page.fill('input[name="result"], input[placeholder*="Result"]', result)
        page.click('button:has-text("Save")')
        
        print(f"✓ Logged {workout_name}: {result}")
        return True
    except Exception as e:
        print(f"✗ Log failed: {e}")
        return False

def view_schedule(page):
    """View gym schedule"""
    print("Loading gym schedule...")
    log("VIEW_SCHEDULE")
    
    try:
        page.goto(f"{WODIFY_BASE_URL}/Schedule")
        page.wait_for_load_state("networkidle")
        
        # Extract schedule info
        classes = page.query_selector_all('.class-item, .wod-item, [data-class]')
        print(f"\nFound {len(classes)} classes:\n")
        
        for cls in classes[:10]:  # Show first 10
            try:
                name = cls.query_selector('.class-name, .wod-name').inner_text()
                time = cls.query_selector('.class-time, .time').inner_text()
                print(f"  {time} - {name}")
            except:
                continue
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def view_history(page):
    """View personal workout history"""
    print("Loading workout history...")
    log("VIEW_HISTORY")
    
    try:
        page.goto(f"{WODIFY_BASE_URL}/Performance")
        page.wait_for_load_state("networkidle")
        
        # Extract history
        workouts = page.query_selector_all('.workout-item, .history-item')
        print(f"\nRecent workouts ({len(workouts)}):\n")
        
        for wod in workouts[:10]:
            try:
                name = wod.query_selector('.workout-name').inner_text()
                date = wod.query_selector('.workout-date, .date').inner_text()
                result = wod.query_selector('.result, .score').inner_text()
                print(f"  {date}: {name} = {result}")
            except:
                continue
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Wodify Member Automation")
    parser.add_argument("--show", action="store_true", help="Show browser window")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Checkin
    checkin_parser = subparsers.add_parser("checkin", help="Check into a WOD")
    checkin_parser.add_argument("wod_name", help="WOD/class name")
    
    # Log workout
    log_parser = subparsers.add_parser("log-workout", help="Log workout result")
    log_parser.add_argument("workout_name", help="Workout name")
    log_parser.add_argument("result", help="Your result/time/score")
    
    # View schedule
    subparsers.add_parser("view-schedule", help="View gym schedule")
    
    # View history
    subparsers.add_parser("view-history", help="View workout history")
    
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
        elif args.command == "checkin":
            checkin_wod(page, args.wod_name)
        elif args.command == "log-workout":
            log_workout(page, args.workout_name, args.result)
        elif args.command == "view-schedule":
            view_schedule(page)
        elif args.command == "view-history":
            view_history(page)
        
    finally:
        close_browser(p, browser, context)

if __name__ == "__main__":
    main()
