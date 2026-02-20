#!/usr/bin/env python3
"""
Update cron jobs with agent hierarchy model assignments

Hierarchy:
- Henry (Coordinator): Opus 4.6 - light work, complex model
- Workers (Scout, Quill, Pixel, Echo, Codex, Daneel): Kimi K2.5 - heavy work
- Haiku (Heartbeat): Gemini Flash - minimal status checks
"""

import json
import sys

JOBS_FILE = "/Users/daneel/.openclaw/cron/jobs.json"

# Model assignments
OPUS_4_6 = "openrouter/anthropic/claude-opus-4-6"
KIMI_K2_5 = "openrouter/moonshotai/kimi-k2.5"
GEMINI_FLASH = "openrouter/google/gemini-3-flash-preview"

# Job categories
HEARTBEAT_JOBS = [
    "Ops - Morning System Check",
    "OpenClaw Update Check", 
    "Email Automation Health Check",
    "Email Check - Daneel's Inbox (Every 30 min)",
    "Email Check - Jason's Blaze Inbox (Every 30 min)",
    "Strategist - Daily Check-in",
    "Builder - Daily Systems Check",
    "Debugger - Daily System Health",
]

WORKER_JOBS_KIMI = [
    "AI News Summary - Daily",
    "Daily Model Usage Check",
]

# Load jobs
with open(JOBS_FILE, 'r') as f:
    data = json.load(f)

updated = 0
for job in data['jobs']:
    if not job.get('enabled'):
        continue
    
    name = job.get('name', '')
    payload = job.get('payload', {})
    current_model = payload.get('model', 'NOT SET')
    
    # Heartbeat jobs → Gemini Flash (cheap, fast)
    if name in HEARTBEAT_JOBS:
        if current_model != GEMINI_FLASH:
            payload['model'] = GEMINI_FLASH
            print(f"🔄 {name}: {current_model} → Gemini Flash")
            updated += 1
        else:
            print(f"✅ {name}: already Gemini Flash")
    
    # Worker jobs missing model → Kimi K2.5
    elif name in WORKER_JOBS_KIMI:
        if current_model != KIMI_K2_5:
            payload['model'] = KIMI_K2_5
            print(f"🔄 {name}: {current_model} → Kimi K2.5")
            updated += 1
        else:
            print(f"✅ {name}: already Kimi K2.5")

# Save if updated
if updated > 0:
    # Backup first
    import shutil
    shutil.copy(JOBS_FILE, JOBS_FILE + '.backup-before-hierarchy')
    
    with open(JOBS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n✅ Updated {updated} jobs. Backup saved.")
else:
    print("\n✅ All jobs already correctly configured.")

print("\n=== NEXT STEPS ===")
print("1. Create Henry coordination job using Opus 4.6")
print("2. Restart openclaw gateway to apply changes")
