#!/usr/bin/env python3
"""
Add nightly 2 AM Mission Advancement task
This task runs every night to build toward the core mission:
"Build an autonomous organization of AI agents that does work for Jason and produces value 24/7"
"""

import json
import uuid
from datetime import datetime

JOBS_FILE = "/Users/daneel/.openclaw/cron/jobs.json"

# The Mission Advancement task - runs every night at 2 AM
mission_task = {
    "id": str(uuid.uuid4()),
    "name": "Mission Advancement - Build Autonomous Org",
    "enabled": True,
    "deleteAfterRun": False,
    "createdAtMs": int(datetime.now().timestamp() * 1000),
    "updatedAtMs": int(datetime.now().timestamp() * 1000),
    "schedule": {
        "kind": "cron",
        "expr": "0 2 * * *",  # 2 AM daily
        "tz": "America/New_York"
    },
    "sessionTarget": "isolated",
    "payload": {
        "kind": "agentTurn",
        "message": """**MISSION: Build Autonomous Organization of AI Agents (2 AM Advancement Task)**

Core Mission: "Build an autonomous organization of AI agents that does work for Jason and produces value 24/7"

**TONIGHT'S ADVANCEMENT CYCLE:**

Read these files to assess current state:
1. `shared-context/priorities.md` - what's the current focus?
2. `shared-context/agent-outputs/` - what did agents accomplish yesterday?
3. `shared-context/kpis/` - current metrics
4. `shared-context/feedback/` - what worked, what didn't?
5. `SESSION-STATE.md` - current operational status

**PICK ONE ADVANCEMENT ACTION (rotate nightly):**

**A. AGENT RECRUITMENT** (Night 1, 8, 15, 22)
- Identify gaps in agent roster
- Design new agent role/role-prompt
- Write agent specification to `shared-context/agent-specs/`
- Example: "We need a Finance agent to track expenses"

**B. AUTOMATION BUILD** (Night 2, 9, 16, 23)
- Find repetitive task that could be automated
- Design cron job or tool to handle it
- Write spec to `shared-context/automation-queue/`
- Example: "Auto-generate daily report from inbox"

**C. PROCESS OPTIMIZATION** (Night 3, 10, 17, 24)
- Review agent outputs from past week
- Identify bottlenecks or inefficiencies
- Propose workflow improvements
- Write to `shared-context/process-improvements/`

**D. CAPABILITY EXPANSION** (Night 4, 11, 18, 25)
- Research new tool/skill/agent that could add value
- Check ClawHub for relevant skills
- Document integration plan
- Write to `shared-context/capability-research/`

**E. KNOWLEDGE CAPTURE** (Night 5, 12, 19, 26)
- Review recent work with Jason
- Extract lessons learned/decisions made
- Update MEMORY.md or relevant docs
- Ensure continuity for future sessions

**F. SYSTEM HARDENING** (Night 6, 13, 20, 27)
- Check for gaps in monitoring/alerting
- Propose reliability improvements
- Document failure modes
- Write to `shared-context/system-hardening/`

**G. VALUE METRICS** (Night 7, 14, 21, 28)
- Calculate value produced this week
- Track agent productivity
- Update KPIs
- Propose value-based improvements

**OUTPUT REQUIREMENTS:**
1. Pick tonight's category (A-G) based on date
2. Execute ONE concrete advancement action
3. Write results to `shared-context/agent-outputs/mission-advancement-YYYY-MM-DD.md`
4. Include: What was done, why it advances the mission, next step

Keep under 1500 chars. Be specific. No vague recommendations.""",
        "timeoutSeconds": 300,
        "model": "openrouter/moonshotai/kimi-k2.5",
        "agent": "Mission Architect"
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

# Check if job already exists
exists = any("Mission Advancement" in job.get('name', '') for job in data['jobs'])

if exists:
    print("⚠️ Mission Advancement task already exists. Updating...")
    # Find and update
    for job in data['jobs']:
        if "Mission Advancement" in job.get('name', ''):
            job['payload'] = mission_task['payload']
            job['updatedAtMs'] = int(datetime.now().timestamp() * 1000)
            print("✅ Updated Mission Advancement task")
            break
else:
    # Add job
    data['jobs'].append(mission_task)
    print("✅ Added Mission Advancement task (2 AM daily)")
    print(f"   Schedule: 2:00 AM every night")
    print(f"   Model: {mission_task['payload']['model']}")
    print(f"   Purpose: Build toward autonomous organization")

# Save
with open(JOBS_FILE, 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✅ Total enabled jobs: {len([j for j in data['jobs'] if j.get('enabled')])}")
print("\nTonight's focus (based on date):")
day = datetime.now().day % 7
focuses = [
    "A. AGENT RECRUITMENT - Identify gaps, design new agent roles",
    "B. AUTOMATION BUILD - Find repetitive tasks, design automation",
    "C. PROCESS OPTIMIZATION - Review outputs, fix bottlenecks",
    "D. CAPABILITY EXPANSION - Research new tools/skills",
    "E. KNOWLEDGE CAPTURE - Document lessons learned",
    "F. SYSTEM HARDENING - Improve reliability, monitoring",
    "G. VALUE METRICS - Track productivity, update KPIs"
]
print(f"   {focuses[day]}")
