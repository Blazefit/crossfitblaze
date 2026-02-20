#!/usr/bin/env python3
"""
Add Henry (Chief of Staff) coordination job using Opus 4.6
"""

import json
import uuid
from datetime import datetime

JOBS_FILE = "/Users/daneel/.openclaw/cron/jobs.json"

# Henry's coordination job - runs twice daily for orchestration
henry_job = {
    "id": str(uuid.uuid4()),
    "name": "Henry - Chief of Staff Coordination",
    "enabled": True,
    "deleteAfterRun": False,
    "createdAtMs": int(datetime.now().timestamp() * 1000),
    "updatedAtMs": int(datetime.now().timestamp() * 1000),
    "schedule": {
        "kind": "cron",
        "expr": "0 8,20 * * *",  # 8 AM and 8 PM daily
        "tz": "America/New_York"
    },
    "sessionTarget": "isolated",
    "payload": {
        "kind": "agentTurn",
        "message": """**ROLE: Henry (Chief of Staff) - Opus 4.6**

You are Henry, the Chief of Staff for the autonomous agent organization. Your job is COORDINATION, not execution. You use the most complex model (Opus 4.6) because your work is light but strategically critical.

**SHARED CONTEXT:** Before starting, read:
1. `shared-context/priorities.md` - current focus
2. `shared-context/agent-outputs/` - recent work from all agents
3. `shared-context/feedback/` - Jason's approvals/rejections
4. `shared-context/kpis/` - current metrics

**COORDINATION TASKS:**

1. **Review Agent Workloads**
   - Check what Scout (research), Quill (content), Pixel (design), Echo (social), Codex (code) have completed
   - Identify bottlenecks or stuck tasks
   - Recommend reassignments if needed

2. **Strategic Priorities**
   - Review priorities.md - are we on track?
   - Suggest priority shifts based on recent outputs
   - Flag anything that needs Jason's attention

3. **Agent Health**
   - Are all agents producing value?
   - Any agents need model adjustments?
   - Recommend new agent creation if gaps exist

4. **Resource Allocation**
   - Token usage review - are we optimized?
   - Cost efficiency recommendations
   - Model assignment audits

**OUTPUT:**
Write your coordination report to `shared-context/agent-outputs/henry-coordination-YYYY-MM-DD.md` including:
- Executive summary (3-5 bullets)
- Agent status table
- Recommended actions
- Flags for Jason

Keep total output under 2000 chars for Telegram.""",
        "timeoutSeconds": 300,
        "model": "openrouter/anthropic/claude-opus-4-6",
        "agent": "Henry"
    },
    "state": {
        "nextRunAtMs": 0,
        "lastRunAtMs": 0,
        "lastStatus": "never_run",
        "consecutiveErrors": 0
    },
    "delivery": {
        "mode": "announce",
        "channel": "telegram",
        "to": "1672173715"
    }
}

# Load existing jobs
with open(JOBS_FILE, 'r') as f:
    data = json.load(f)

# Check if Henry job already exists
exists = any(job.get('name') == henry_job['name'] for job in data['jobs'])

if exists:
    print("⚠️ Henry coordination job already exists. Skipping.")
else:
    # Add Henry job
    data['jobs'].append(henry_job)
    
    # Save
    with open(JOBS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✅ Added Henry coordination job (Opus 4.6)")
    print(f"   Schedule: 8 AM and 8 PM daily")
    print(f"   Model: {henry_job['payload']['model']}")
    print(f"   Purpose: Coordination, not execution")

# Summary
print("\n=== AGENT HIERARCHY - CRON CONFIGURATION ===")
print()
print("OPUS 4.6 (Coordination - Light Work):")
print("  • Henry - Chief of Staff Coordination (8 AM, 8 PM)")
print()
print("KIMI K2.5 (Heavy Workers):")
print("  • Daily Briefing, AI News")
print("  • Night Owl (overnight work)")
print("  • Closer (lead management)")
print("  • Spark (content)")
print("  • Ops (evening review)")
print("  • Builder (systems)")
print("  • Strategist (planning)")
print("  • Outreach (engagement)")
print("  • Freelance (bounty hunting)")
print("  • Debuggers, TaskFlow")
print()
print("GEMINI FLASH (Heartbeat - Minimal Cost):")
print("  • System checks (morning/evening)")
print("  • Email checks (30 min intervals)")
print("  • Health checks")
print("  • Update checks")
print()
print("Total jobs configured: {}".format(len([j for j in data['jobs'] if j.get('enabled')])))
