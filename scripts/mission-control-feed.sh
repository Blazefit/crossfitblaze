#!/bin/bash
# mission-control-feed.sh
# This script runs after key cron jobs to feed their output into Mission Control
# Should be called by cron jobs on successful completion

AGENT_NAME="$1"
OUTPUT_FILE="$2"
STATUS="${3:-ok}"

if [ -z "$AGENT_NAME" ] || [ -z "$OUTPUT_FILE" ]; then
    echo "Usage: $0 <agent_name> <output_file> [status]"
    exit 1
fi

# Write heartbeat
cd /Users/daneel/.openclaw/workspace/mission-control-v2
node -e "
const fs = require('fs');
const path = require('path');

const heartbeatDir = '/Users/daneel/.openclaw/workspace/shared-context/agent-heartbeats';
if (!fs.existsSync(heartbeatDir)) {
    fs.mkdirSync(heartbeatDir, { recursive: true });
}

const heartbeat = {
    agent: '$AGENT_NAME',
    timestamp: new Date().toISOString(),
    status: '$STATUS',
    outputFile: '$OUTPUT_FILE',
    unix_ms: Date.now()
};

fs.writeFileSync(
    path.join(heartbeatDir, '$AGENT_NAME.last'),
    JSON.stringify(heartbeat, null, 2)
);

console.log('Heartbeat written for $AGENT_NAME');
"

# If successful, also add activity to Mission Control
if [ "$STATUS" = "ok" ]; then
    npx convex run activity:create "{\"action\":\"Cron completed\",\"agentId\":\"k170wp66j85b9fe0024xs3jz7h81hn8f\",\"details\":\"$AGENT_NAME completed successfully\"}" 2>/dev/null || true
fi

echo "Mission Control feed updated for $AGENT_NAME"
