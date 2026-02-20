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
