# Feedback Log

Jason's approvals and rejections. Every agent reads this to learn preferences.

## Format

Weekly files: `feedback-YYYY-WXX.json`

```json
[
  {
    "date": "2026-02-11",
    "agent": "main",
    "action": "content suggestion",
    "decision": "approved|rejected",
    "reason": "not high intent",
    "context": "brief description"
  }
]
```

## How Agents Use This

Before recommending anything, check recent feedback for patterns:
- Rejected patterns → avoid similar suggestions
- Approved patterns → weight toward similar approaches
- Reasons → the WHY matters more than the yes/no
