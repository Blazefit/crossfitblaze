#!/bin/bash
#
# Dead Agent Alert System - Setup Script
#
# This script:
# 1. Creates necessary directories
# 2. Generates agent manifest from cron jobs
# 3. Makes scripts executable
# 4. Tests the dead-agent-check logic
# 5. Provides integration instructions
#

set -e

echo "🚀 Dead Agent Alert System - Setup"
echo "===================================="
echo ""

WORKSPACE="$HOME/.openclaw/workspace"
HEARTBEAT_DIR="$WORKSPACE/shared-context/agent-heartbeats"
ALERTS_DIR="$WORKSPACE/shared-context/alerts"
MANIFEST_PATH="$WORKSPACE/shared-context/agent-manifest.json"

# Step 1: Create directories
echo "📁 Creating directories..."
mkdir -p "$HEARTBEAT_DIR"
mkdir -p "$ALERTS_DIR"
echo "   ✅ $HEARTBEAT_DIR"
echo "   ✅ $ALERTS_DIR"
echo ""

# Step 2: Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x "$WORKSPACE/shared-context/system-hardening/generate-manifest.js"
chmod +x "$WORKSPACE/scripts/write-heartbeat.js"
chmod +x "$WORKSPACE/scripts/dead-agent-check.js"
echo "   ✅ Scripts are now executable"
echo ""

# Step 3: Generate manifest
echo "📋 Generating agent manifest..."
node "$WORKSPACE/shared-context/system-hardening/generate-manifest.js"
echo ""

# Step 4: Verify manifest was created
if [ ! -f "$MANIFEST_PATH" ]; then
    echo "❌ Error: Manifest not created at $MANIFEST_PATH"
    exit 1
fi

AGENT_COUNT=$(node -e "console.log(require('$MANIFEST_PATH').total_agents)")
echo "✅ Manifest created with $AGENT_COUNT agents"
echo ""

# Step 5: Create some test heartbeats
echo "🧪 Creating test heartbeats..."

# Create a fresh heartbeat (should be alive)
node "$WORKSPACE/scripts/write-heartbeat.js" "test-agent-alive" "ok" "Test heartbeat - fresh"

# Create an old heartbeat (should be dead)
# We'll manually create this with an old timestamp
cat > "$HEARTBEAT_DIR/test-agent-dead.last" <<EOF
{
  "agent": "test-agent-dead",
  "timestamp": "2026-02-18T12:00:00.000Z",
  "status": "ok",
  "message": "Test heartbeat - old",
  "unix_ms": 1739887200000
}
EOF

echo "   ✅ Created test-agent-alive (fresh)"
echo "   ✅ Created test-agent-dead (48h old)"
echo ""

# Step 6: Run dead agent check
echo "🔍 Running dead agent check (test mode)..."
echo ""
node "$WORKSPACE/scripts/dead-agent-check.js" --report-all || true
echo ""

# Step 7: Show latest alert report
LATEST_REPORT=$(ls -t "$ALERTS_DIR"/dead-agents-*.md | head -n 1)
if [ -n "$LATEST_REPORT" ]; then
    echo "📄 Latest alert report:"
    echo "   $LATEST_REPORT"
    echo ""
    echo "Preview:"
    head -n 20 "$LATEST_REPORT"
    echo ""
fi

# Step 8: Clean up test heartbeats
echo "🧹 Cleaning up test heartbeats..."
rm -f "$HEARTBEAT_DIR/test-agent-alive.last"
rm -f "$HEARTBEAT_DIR/test-agent-dead.last"
echo "   ✅ Test files removed"
echo ""

# Step 9: Integration instructions
echo "✅ Setup complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📖 NEXT STEPS - INTEGRATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  ADD HEARTBEAT CALLS TO AGENTS"
echo ""
echo "For each cron job agent, add this at the END of their successful execution:"
echo ""
echo "   node ~/.openclaw/workspace/scripts/write-heartbeat.js <agent-name> ok \"Brief message\""
echo ""
echo "Example for 'Daily Briefing 5am' job:"
echo "   node ~/.openclaw/workspace/scripts/write-heartbeat.js briefing-daily ok \"Briefing sent\""
echo ""
echo "Add to agent message AFTER completing work:"
echo "   After writing your output to shared-context/agent-outputs/,"
echo "   call write-heartbeat.js with your agent name."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "2️⃣  CREATE DEAD-AGENT-CHECK CRON JOB"
echo ""
echo "Add this job to ~/.openclaw/cron/jobs.json:"
echo ""
cat <<'CRONJSON'
{
  "id": "dead-agent-monitor",
  "name": "Dead Agent Monitor",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "0 */4 * * *",
    "tz": "America/New_York"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run dead agent check: node ~/.openclaw/workspace/scripts/dead-agent-check.js --critical-only. If any dead agents found, alert immediately with details from the generated report.",
    "model": "openrouter/google/gemini-3-flash-preview",
    "timeoutSeconds": 120
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "1672173715"
  }
}
CRONJSON
echo ""
echo "This will check every 4 hours for dead agents."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "3️⃣  MANUAL TESTING"
echo ""
echo "Test commands:"
echo ""
echo "  # List all heartbeats"
echo "  node ~/.openclaw/workspace/scripts/write-heartbeat.js --list"
echo ""
echo "  # Check for dead agents"
echo "  node ~/.openclaw/workspace/scripts/dead-agent-check.js"
echo ""
echo "  # Check critical agents only"
echo "  node ~/.openclaw/workspace/scripts/dead-agent-check.js --critical-only"
echo ""
echo "  # Full report with all agents"
echo "  node ~/.openclaw/workspace/scripts/dead-agent-check.js --report-all"
echo ""
echo "  # Regenerate manifest after cron changes"
echo "  node ~/.openclaw/workspace/shared-context/system-hardening/generate-manifest.js"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📂 FILE LOCATIONS"
echo ""
echo "  Manifest:     $MANIFEST_PATH"
echo "  Heartbeats:   $HEARTBEAT_DIR/"
echo "  Alert Reports: $ALERTS_DIR/"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 Dead Agent Alert System is ready!"
echo ""
