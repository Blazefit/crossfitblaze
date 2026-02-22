#!/bin/bash
# Overnight Wodify Worker - Runs until completion
# Uses Kimi 2.5 exclusively

cd ~/.openclaw/workspace/skills/wodify-browser-automation

# Log file
LOGFILE="agent-task/overnight-log-$(date +%Y%m%d-%H%M).txt"
mkdir -p agent-task

echo "=== OVERNIGHT WODIFY WORK STARTED $(date) ===" | tee -a $LOGFILE
echo "Model: Kimi K2.5" | tee -a $LOGFILE
echo "" | tee -a $LOGFILE

# Function to log and execute
log_exec() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a $LOGFILE
}

# Phase 1: Fix browser issues
log_exec "Phase 1: Fixing browser stability..."
source venv/bin/activate

# Test login
log_exec "Testing Wodify login..."
python3 wodify.py test-login 2>&1 | tee -a $LOGFILE
LOGIN_STATUS=${PIPESTATUS[0]}

if [ $LOGIN_STATUS -ne 0 ]; then
    log_exec "ERROR: Login failed. Browser fixes needed."
    echo "Attempting to fix browser issues..." | tee -a $LOGFILE
    # Will need to update script
fi

# Phase 2: Extract prices
log_exec "Phase 2: Extracting membership prices..."

# Try to use existing session to get prices
python3 << 'PYEOF'
import json
import sys
sys.path.insert(0, '.')
from wodify import create_browser, close_browser, login, load_credentials

creds = load_credentials()
p, browser, context, page, has_session = create_browser(headless=True)

try:
    if login(page, creds):
        print("✓ Logged in successfully")
        
        # Try to navigate to contracts
        urls_to_try = [
            "https://app.wodify.com/Admin/Main?q=Contracts",
            "https://app.wodify.com/Admin/Main?q=MembershipPlans",
            "https://app.wodify.com/Admin/Main?q=Programs",
        ]
        
        for url in urls_to_try:
            print(f"\nTrying: {url}")
            page.goto(url)
            page.wait_for_timeout(5000)
            
            # Get page title
            title = page.title()
            print(f"Page title: {title}")
            print(f"URL: {page.url}")
            
            # Try to extract text content
            content = page.content()
            if "membership" in content.lower() or "plan" in content.lower() or "price" in content.lower():
                print("Found relevant page!")
                # Save content for analysis
                with open(f"agent-task/page-content-{url.split('=')[1]}.html", "w") as f:
                    f.write(content)
                break
    else:
        print("✗ Login failed")
        sys.exit(1)
finally:
    close_browser(p, browser, context)
PYEOF

log_exec "Price extraction attempt complete."

# Check what was found
if [ -f agent-task/page-content-*.html ]; then
    log_exec "Page content saved. Analyzing..."
    # Extract prices from HTML
    grep -iE "unlimited|basic|drop|month|\$[0-9]+" agent-task/page-content-*.html | head -20 | tee -a $LOGFILE
fi

# Phase 3: Update script with what we found
log_exec "Phase 3: Updating add-member.py..."
# This will be done once prices are confirmed

echo "" | tee -a $LOGFILE
echo "=== WORK COMPLETE $(date) ===" | tee -a $LOGFILE
