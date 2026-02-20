# Dead Agent Alert System

**Created:** 2026-02-20
**Category:** System Hardening
**Priority:** HIGH

## Problem

32 cron jobs run daily. When they fail, nobody knows:
- No stdout/stderr capture
- No timestamp verification of outputs
- Silent failures on API changes, auth expiry, config drift
- 3 jobs already broken (Gmail→Zoho migration incomplete)

## Failure Mode Documented

**Example:** `blazeinbox-daily` cron job. If Zoho auth expires:
- Job runs, fails silently
- No inbox check occurs
- Jason misses urgent emails
- No one knows until Jason manually checks

## Proposed Solution: Dead Agent Alert

### Component 1: Agent Heartbeat Registry
Each agent writes a timestamp file on successful completion:
```
shared-context/agent-heartbeats/
├── briefing-daily.last
├── blazeinbox-daily.last
├── spark-content.last
└── ...
```

Format: `ISO8601 timestamp + exit status`

### Component 2: Dead Agent Monitor (New Cron Job)
**Schedule:** Every 4 hours
**Job:** `dead-agent-check`
**Model:** Gemini Flash (cheap, frequent)

**Logic:**
```
for each registered agent:
  read last heartbeat timestamp
  if (now - timestamp) > expected_interval * 1.5:
    add to dead_agents list

if dead_agents not empty:
  write alert to shared-context/alerts/dead-agents-YYYY-MM-DD-HH.md
  include: agent name, expected vs actual last run, likely cause
```

### Component 3: Agent Registration Manifest
Single source of truth in `shared-context/agent-manifest.json`:
```json
{
  "agents": [
    {
      "name": "briefing-daily",
      "cron": "0 5 * * *",
      "expected_interval_hours": 24,
      "output_path": "shared-context/agent-outputs/briefing-daily-*.md",
      "dependencies": ["zoho-mail"]
    },
    {
      "name": "blazeinbox-daily",
      "cron": "0 6 * * *",
      "expected_interval_hours": 24,
      "output_path": "shared-context/agent-outputs/blazeinbox-*.md",
      "dependencies": ["zoho-mail"]
    }
  ]
}
```

## Implementation Steps

1. **Create manifest** from existing cron jobs (audit required)
2. **Modify top 5 critical agents** to write heartbeat on success
3. **Build dead-agent-check** cron job
4. **Test** by manually aging a heartbeat file
5. **Roll out** to all agents gradually

## Immediate Actions Taken Tonight

- [x] Documented failure mode
- [x] Designed detection system
- [x] Created system-hardening directory structure

## Next Step

Build `shared-context/agent-manifest.json` by auditing all 32 cron jobs. Estimated 30 min work.

---

**Impact:** Prevents silent failures. Knows when agents die within 4 hours instead of discovering accidentally days later.
