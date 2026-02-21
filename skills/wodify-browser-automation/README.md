# Wodify Browser Automation

Manage CrossFit Blaze gym members through Wodify's admin interface using browser automation.

## Quick Start

1. **Install dependencies:**
   ```bash
   cd ~/.openclaw/workspace/skills/wodify-browser-automation
   pip install -r requirements.txt
   playwright install chromium
   ```

2. **Configure credentials:**
   ```bash
   mkdir -p ~/.wodify
   cp config.template.json ~/.wodify/credentials.json
   # Edit ~/.wodify/credentials.json with your Wodify login
   ```

3. **Run commands:**
   ```bash
   python3 wodify.py list-clients
   python3 wodify.py add-client "Jane Smith" "jane@email.com" "239-555-1234"
   ```

## Commands

| Command | Description |
|---------|-------------|
| `add-client "Name" "Email" "Phone"` | Add a new member |
| `list-clients` | List all active clients |
| `search "Name"` | Search for a client |
| `hold-client "Name" "Reason"` | Put membership on hold |
| `remove-client "Name"` | Remove/cancel membership |

## Options

- `--show` - Show browser window (default is headless)

## Examples

```bash
# Add a new client
python3 wodify.py add-client "John Doe" "john@email.com" "239-555-1234"

# List all clients
python3 wodify.py list-clients

# Search for a client
python3 wodify.py search "John"

# Put on hold
python3 wodify.py hold-client "John Doe" "Vacation - 2 weeks"

# Remove client
python3 wodify.py remove-client "John Doe"

# Show browser while running
python3 wodify.py --show list-clients
```

## Files

- `wodify.py` - Main CLI tool
- `SKILL.md` - OpenClaw skill documentation
- `config.template.json` - Credential template
- `requirements.txt` - Python dependencies

## Logs

All activity is logged to `~/.wodify/activity.log`
