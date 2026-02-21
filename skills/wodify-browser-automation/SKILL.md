---
name: wodify-browser-automation
description: Manage Wodify gym members via browser automation (add, remove, hold clients). No API required - uses Playwright to automate the Wodify admin interface.
homepage: https://wodify.com
metadata:
  openclaw:
    emoji: 🏋️
    requires:
      bins: ["python3", "playwright"]
      env: []
---

# Wodify Browser Automation

Manage CrossFit Blaze members through Wodify's admin interface using browser automation.

## Setup

1. Install dependencies:
```bash
pip install playwright
playwright install chromium
```

2. Create credentials file:
```bash
mkdir -p ~/.wodify
cp config.template.json ~/.wodify/credentials.json
# Edit ~/.wodify/credentials.json with your Wodify login
```

## Commands

```bash
# Add a new client
python3 wodify.py add-client "John Doe" "john@email.com" "239-555-1234"

# List all active clients
python3 wodify.py list-clients

# Search for a client
python3 wodify.py search "John"

# Put a client on hold
python3 wodify.py hold-client "John Doe" "Vacation - 2 weeks"

# Remove/cancel a client
python3 wodify.py remove-client "John Doe"
```

## Features

- **Session persistence**: Saves cookies to avoid repeated logins
- **Headless mode**: Runs in background by default
- **Interactive mode**: Use `--show` flag to see the browser
- **Retry logic**: Automatically retries on transient errors

## Configuration

Edit `~/.wodify/credentials.json`:

```json
{
  "email": "your-email@example.com",
  "password": "your-password",
  "gym_id": "crossfitblaze"
}
```

## Notes

- First run will be slower (needs to login)
- Subsequent runs reuse session cookies
- Uses Chromium browser in headless mode
- All actions are logged to `~/.wodify/activity.log`
