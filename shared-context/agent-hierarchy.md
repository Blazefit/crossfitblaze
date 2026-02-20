# Agent Hierarchy & Model Assignments

**Last Updated:** 2026-02-20
**Purpose:** Define model assignments for autonomous agent organization

## Core Principle
- **Coordinator (least work)** → Most complex model (Opus 4.6)
- **Heavy workers (data entry, research, coding)** → Efficient models (Kimi K2.5)
- **Heartbeat monitors** → Lightest/cheapest models (Haiku, Gemini Flash)

## Agent Roster

| Agent | Role | Model | Purpose | Workload |
|-------|------|-------|---------|----------|
| **Henry** | Chief of Staff | **Opus 4.6** | Orchestration, delegation, strategic decisions | Light (coordination only) |
| **Scout** | Research Analyst | **Kimi K2.5** | Bounty hunting, lead research, trend analysis | Heavy |
| **Quill** | Content Writer | **Kimi K2.5** | Writing, copy, captions, scripts | Heavy |
| **Pixel** | Thumbnail Designer | **Kimi K2.5** | Graphics, thumbnails, visuals | Heavy |
| **Echo** | Social Media Manager | **Kimi K2.5** | Posting, engagement, scheduling | Heavy |
| **Codex** | Code Engineer | **Kimi K2.5** | Tools, APIs, automations | Heavy |
| **Daneel** | AI Assistant | **Kimi K2.5** | Main interface, task execution | Heavy |
| **Haiku** | Heartbeat Monitor | **Gemini Flash** | Status checks, lightweight polls | Minimal |

## Model Routing (OpenRouter)

```bash
# Opus 4.6 (Henry only)
openrouter/anthropic/claude-opus-4-6

# Kimi K2.5 (Most agents)
openrouter/moonshotai/kimi-k2.5

# Gemini Flash (Haiku/heartbeat)
openrouter/google/gemini-flash-1.5

# Haiku alternative (if needed)
openrouter/anthropic/claude-haiku
```

## Cost Optimization

| Model | Relative Cost | Use Case |
|-------|---------------|----------|
| Opus 4.6 | $$$$ | Complex reasoning, coordination |
| Kimi K2.5 | $$ | Daily work, heavy tasks |
| Gemini Flash | $ | Heartbeats, simple checks |
| Haiku | $ | Fallback for lightweight tasks |

## Decision Tree

1. Is this a **coordination/orchestration** task? → **Henry (Opus 4.6)**
2. Is this a **heartbeat/status check**? → **Haiku (Gemini Flash)**
3. Is this **production work** (research, writing, coding)? → **Kimi K2.5**
4. Is this a **complex analysis** requiring deep reasoning? → Escalate to Henry

## Implementation Notes

- All agents route through OpenRouter
- API keys stored in environment: `OPENROUTER_API_KEY`
- Model switching happens at spawn time via `--model` flag
- Henry delegates to specialists, doesn't do heavy lifting
- Cost savings: ~70% by using Kimi for bulk work vs Opus

## Mission Advancement Job (2 AM Daily)

**Job:** Mission Advancement - Build Autonomous Org  
**Schedule:** 2:00 AM daily  
**Model:** Kimi K2.5  
**Agent:** Mission Architect  

**Purpose:** Directly advances the core mission: "Build an autonomous organization of AI agents that does work for Jason and produces value 24/7"

**Rotating Focus (cycles weekly):**
1. **Agent Recruitment** - Identify gaps, design new agent roles, write specs
2. **Automation Build** - Find repetitive tasks, design automations
3. **Process Optimization** - Review outputs, fix bottlenecks
4. **Capability Expansion** - Research new tools/skills on ClawHub
5. **Knowledge Capture** - Document lessons learned, update MEMORY.md
6. **System Hardening** - Improve monitoring, reliability
7. **Value Metrics** - Track productivity, update KPIs

**Output:** Written to `shared-context/agent-outputs/mission-advancement-YYYY-MM-DD.md`

This ensures every night we're one step closer to full autonomy.
