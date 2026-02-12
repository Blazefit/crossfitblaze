# Setup Improvement Plan — Based on OpenAI Agent Primitives Blog
**Source:** https://developers.openai.com/blog/skills-shell-tips
**Date:** 2026-02-11

## What the article covers
OpenAI released new agent primitives: Skills, Shell (execution environments), and Server-side Compaction. 10 tips for long-running multi-hour workflows.

## What we already do well ✅
- **Skills architecture** — We already use ClawHub skills (upload-post, delx, himalaya, etc.)
- **Shared context** — Our shared-context/ directory IS the "skills + templates" pattern they describe
- **Compaction** — OpenClaw has safeguard compaction mode enabled
- **File-based handoffs** — Our agent-outputs/ pattern matches their "/mnt/data as handoff boundary"
- **Local execution** — We run everything on the Mac mini with full shell access

## What we should improve 🎯

### 1. Skill descriptions need "routing logic" not marketing copy
**Current:** Our cron jobs have long inline prompts
**Fix:** Move each agent's instructions into proper SKILL.md files with:
- "Use when..." / "Don't use when..." blocks
- Negative examples to prevent misfires
- Success criteria for each agent

### 2. Templates inside skills, not system prompts
**Current:** Email templates, content formats, lead scripts are scattered
**Fix:** Create skill bundles per agent role:
- `skills/closer/` — lead templates, follow-up scripts, conversion playbooks
- `skills/spark/` — content templates, hashtag sets, caption formats
- `skills/ops/` — health check procedures, troubleshooting runbooks
- Templates only load when the agent runs (saves tokens)

### 3. Better compaction strategy
**Current:** safeguard mode (compacts only when hitting limits)
**Fix:** Consider switching to proactive compaction for long sessions
- Main session gets very long on busy days like today
- Pre-compaction memory flushes help but we could be more aggressive

### 4. Negative examples for agent routing
**Current:** Agents sometimes overlap (Closer and Outreach both touch leads)
**Fix:** Add explicit "Don't do X" rules:
- Closer: "Don't do general member engagement — that's Outreach"
- Outreach: "Don't handle new lead inquiries — that's Closer"  
- Spark: "Don't draft email replies — that's the email agents"

### 5. Artifact handoff boundaries
**Current:** Agents write to shared-context/agent-outputs/ ✅
**Improvement:** Standardize output format across all agents:
```
# Agent Output — {agent}-{type}-{date}
## Summary (1-2 lines)
## Key Findings
## Action Items (numbered)
## Files Created/Modified
## Next Agent Action Needed
```

### 6. Security: Treat skills + networking as high-risk
**Current:** Cron jobs have API keys in plaintext in prompts
**Fix:** Move secrets to environment variables, not prompt text
- OpenWork API key in cron prompts → env var
- Upload-Post API key → env var
- Himalaya passwords → already in config (good)

## Implementation Priority

| # | Improvement | Effort | Impact | Do When |
|---|-----------|--------|--------|---------|
| 1 | Standardize agent output format | Low | Medium | This week |
| 2 | Add negative examples to agents | Low | High | This week |
| 3 | Move API keys out of prompts | Medium | High | This week |
| 4 | Create skill bundles per agent | Medium | High | Next week |
| 5 | Templates inside skills | Medium | Medium | Next week |
| 6 | Proactive compaction review | Low | Medium | When needed |
