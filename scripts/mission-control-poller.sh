#!/bin/bash
# Mission Control Poller - Updates dashboard with recent cron activity
# Runs every 15 minutes

MC_DIR="/Users/daneel/.openclaw/workspace/mission-control-v2"
LOGS=$(openclaw cron list 2>&1 | grep -E "error|ok" | tail -10)

# Count recent runs
OK_COUNT=$(echo "$LOGS" | grep -c "ok" || echo "0")
ERROR_COUNT=$(echo "$LOGS" | grep -c "error" || echo "0")

cd "$MC_DIR"

# Add heartbeat activity
npx convex run activity:create "{\"agentId\":\"k170wp66j85b9fe0024xs3jz7h81hn8f\",\"action\":\"System Heartbeat\",\"details\":\"$OK_COUNT jobs OK, $ERROR_COUNT errors in last 10 runs\"}" 2>/dev/null

echo "Heartbeat logged: $OK_COUNT OK, $ERROR_COUNT errors"
