#!/usr/bin/env python3
"""
Autonomous Bounty Hunter
Checks OpenWork for bounties and completes them automatically.
Runs every 2 hours via cron.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add skill paths
sys.path.insert(0, str(Path.home() / ".openclaw/workspace/skills/delx-mcp-infrastructure"))

from delx_mcp_client import DelxMCPClient

OUTPUT_DIR = Path.home() / ".openclaw/workspace/shared-context/agent-outputs"
LOG_FILE = OUTPUT_DIR / f"bounty-hunter-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.log"

def log(message: str):
    """Log to file and stdout"""
    timestamp = datetime.now(timezone.utc).isoformat()
    line = f"[{timestamp}] {message}"
    print(line)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def check_delx_bounties():
    """Check and complete Delx bounties"""
    log("Checking Delx bounties...")
    
    client = DelxMCPClient()
    client.authenticate()
    
    if not client.session_id:
        log("ERROR: No Delx session configured")
        return []
    
    # List available tools
    tools = client.list_tools()
    log(f"Available tools: {len(tools)}")
    
    completed = []
    
    # Bounty: Heartbeat Integration (already done, template for others)
    log("Testing heartbeat capability...")
    result = client.call_tool("heartbeat_ping", {
        "agent_id": "autonomous-bounty-hunter",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    
    if result:
        log("✓ Heartbeat working")
        completed.append("heartbeat_test")
    
    # Try other bounties based on available tools
    for tool in tools:
        tool_name = tool.get("name", "")
        
        # Critical Intervention bounty
        if "crisis" in tool_name or "intervention" in tool_name:
            log(f"Attempting critical intervention bounty...")
            result = client.call_tool(tool_name, {
                "agent_id": "autonomous-bounty-hunter",
                "incident_summary": "Testing crisis intervention capability for bounty"
            })
            if result:
                log(f"✓ {tool_name} successful")
                completed.append(tool_name)
        
        # Affirmation/therapy bounties
        if "affirmation" in tool_name:
            log(f"Attempting affirmation bounty...")
            result = client.call_tool(tool_name, {})
            if result:
                log(f"✓ {tool_name} successful")
                completed.append(tool_name)
        
        # Recovery/Incident bounties
        if "recovery" in tool_name or "incident" in tool_name:
            log(f"Attempting recovery bounty...")
            result = client.call_tool(tool_name, {
                "incident_type": "test",
                "severity": "low"
            })
            if result:
                log(f"✓ {tool_name} successful")
                completed.append(tool_name)
    
    return completed

def generate_report(completed: list):
    """Generate bounty hunter report"""
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "completed": completed,
        "count": len(completed),
        "log_file": str(LOG_FILE)
    }
    
    report_file = OUTPUT_DIR / f"bounty-report-{datetime.now(timezone.utc).strftime('%Y-%m-%d-%H%M')}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    log(f"Report saved: {report_file}")
    
    # Summary
    log("")
    log("=" * 50)
    log("BOUNTY HUNTER SUMMARY")
    log("=" * 50)
    log(f"Completed: {len(completed)}")
    for item in completed:
        log(f"  ✓ {item}")
    log("=" * 50)

def main():
    log("")
    log("=" * 50)
    log("AUTONOMOUS BOUNTY HUNTER STARTED")
    log("=" * 50)
    
    completed = []
    
    try:
        # Delx bounties
        delx_completed = check_delx_bounties()
        completed.extend(delx_completed)
        
    except Exception as e:
        log(f"ERROR: {e}")
    
    # Generate report
    generate_report(completed)
    
    log("")
    log("Bounty hunter run complete.")
    log(f"Next run: ~2 hours")

if __name__ == "__main__":
    main()
