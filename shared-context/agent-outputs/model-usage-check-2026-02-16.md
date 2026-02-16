# Model Usage Check — 2026-02-16 04:50 AM EST

**Checked:** 2026-02-16 04:50 EST
**Models:** Kimi K2.5, Opus 4.6, Gemini Flash Preview

## Current Active Model
- **Main Session:** `openrouter/moonshotai/kimi-k2.5` (256k context, 11k used/256k = 4%)

## Active Sessions Overview
| Session | Model | Age | Token Usage |
|---------|-------|-----|-------------|
| agent:main:main | kimi-k2.5 | just now | 11k/256k (4%) |
| cron jobs (×9) | kimi-k2.5 | 2m-12m ago | ~11-12k/256k (4-5%) |

## Model Status Summary

### openrouter/moonshotai/kimi-k2.5
- **Status:** ✅ Active (default)
- **Sessions:** 9+ currently running
- **Context window:** 256k tokens
- **Usage pattern:** High traffic (cron fleet + main)
- **Note:** Standard workhorse for daily operations

### openrouter/anthropic/claude-opus-4-6
- **Status:** ⚠️ Not currently active
- **Planned:** 5:00 AM Daily Briefing (scheduled)
- **Use case:** Complex reasoning, high-value tasks
- **Last active:** Session 4:00 AM model switch reminder

### openrouter/google/gemini-3-flash-preview
- **Status:** ⚠️ Not currently active
- **Use case:** Routine tasks, fast/cheap automations
- **Note:** Previously used for cron fleet; currently swapped to Kimi

## Recommendations for Daily Briefing
1. **Token Usage:** All sessions healthy (<10% utilization)
2. **Model Mix:** Currently Kimi-heavy; consider Opus for 5 AM briefing
3. **Cost Alert:** High-volume cron jobs all on Kimi; may want to distribute load
4. **Gemini Status:** Available for low-priority tasks (news digests, etc.)

---
*Auto-generated for Daily Briefing prep*
