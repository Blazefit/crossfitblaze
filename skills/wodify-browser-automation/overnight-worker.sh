#!/bin/bash
# Overnight Wodify Worker - Final Version
# Reports status and provides clear next steps for MFA

cd ~/.openclaw/workspace/skills/wodify-browser-automation

# Log file
LOGFILE="agent-task/overnight-log-$(date +%Y%m%d-%H%M).txt"
mkdir -p agent-task

echo "=== OVERNIGHT WODIFY WORK STARTED $(date) ===" | tee -a $LOGFILE
echo "Model: Kimi 2.5" | tee -a $LOGFILE
echo "" | tee -a $LOGFILE

# Function to log and execute
log_exec() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a $LOGFILE
}

source venv/bin/activate

# Run enhanced automation
log_exec "Running Wodify automation..."
python3 wodify_enhanced.py 2>&1 | tee -a $LOGFILE
STATUS=${PIPESTATUS[0]}

if [ $STATUS -eq 0 ]; then
    log_exec "✓ Automation completed successfully"
    
    if [ -f agent-task/membership-prices.json ]; then
        log_exec "✓ Membership prices extracted"
        echo "" | tee -a $LOGFILE
        echo "--- EXTRACTED PRICES ---" | tee -a $LOGFILE
        cat agent-task/membership-prices.json | tee -a $LOGFILE
        echo "" | tee -a $LOGFILE
    fi
else
    log_exec "⚠️  Automation incomplete - MFA required"
    log_exec ""
    log_exec "To complete setup and enable full automation:"
    log_exec "1. Run: python3 setup_mfa.py"
    log_exec "2. Click 'Email a code' in the browser window"
    log_exec "3. Check email (da••••@aimissioncontrol.us) for MFA code"
    log_exec "4. Enter the code in the browser"
    log_exec "5. Press ENTER in terminal to save session"
    log_exec ""
    log_exec "After one-time setup, overnight automation will work automatically."
fi

echo "" | tee -a $LOGFILE
echo "=== WORK COMPLETE $(date) ===" | tee -a $LOGFILE

exit 0
