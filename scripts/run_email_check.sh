#!/bin/bash
# Load GMAIL_APP_PASSWORD from a persistent env file if it exists
if [ -f "/Users/daneel/.openclaw/workspace/.env" ]; then
    export $(grep -v '^#' /Users/daneel/.openclaw/workspace/.env | xargs)
fi
python3 /Users/daneel/.openclaw/workspace/scripts/check_inbox.py
