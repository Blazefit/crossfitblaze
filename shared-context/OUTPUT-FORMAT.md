# Agent Output Standard Format

All agents must write outputs to `shared-context/agent-outputs/` using this format:

**Filename:** `{agent}-{type}-{YYYY-MM-DD}.md`

**Template:**
# {Agent Name} — {Type} — {Date}

## Summary
1-2 line overview of what was done/found.

## Key Findings
- Bullet points of important discoveries or completions

## Action Items
1. Numbered list of things that need attention
2. Tag who should handle it: [Jason] [Closer] [Spark] etc.

## Files Created/Modified
- List any files written or changed

## Cross-Agent Signals
- Any info other agents should know about
- E.g., "Found keyword opportunity" → Spark should create content
- E.g., "New lead detected" → Closer should follow up
