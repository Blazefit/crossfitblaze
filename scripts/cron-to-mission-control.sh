#!/bin/bash
# This script pipes cron job output to Mission Control
# Usage: <cron command> | cron-to-mission-control.sh <agent_name>

AGENT_NAME="${1:-Unknown}"
OUTPUT=$(cat)

echo "$OUTPUT"

# Also send to Mission Control
if command -v npx &> /dev/null; then
    cd /Users/daneel/.openclaw/workspace/mission-control-v2 2>/dev/null || exit 0
    # Truncate output for Mission Control
    SUMMARY=$(echo "$OUTPUT" | head -c 500)
    npx convex run activity:create "{\"agentId\":\"k170wp66j85b9fe0024xs3jz7h81hn8f\",\"action\":\"$AGENT_NAME completed\",\"details\":\"$SUMMARY\"}" 2>/dev/null || true
fi
