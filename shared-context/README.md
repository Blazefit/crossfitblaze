# shared-context/

The shared brain. Every agent reads from here. One directory, same files, no silos.

## Structure

```
shared-context/
├── priorities.md          ← Current priority stack (updated from Jason's input)
├── agent-outputs/         ← Each agent/cron drops results here. Others read them.
├── feedback/              ← Jason's approvals + rejections flow to ALL agents
├── kpis/                  ← Live metrics any agent can reference
└── content-calendar/      ← What's planned, published, and gaps
```

## Rules

1. **Read `priorities.md` before every action.** It's the source of truth.
2. **Drop your output in `agent-outputs/`** with format: `{agent}-{type}-{date}.md`
3. **Check `feedback/`** for recent approvals/rejections before making recommendations.
4. **Never delete** — append, update, or archive. Git tracks everything.

## Adding a New Agent

1. Symlink this directory into the agent's workspace
2. Add to agent instructions: "Read shared-context/ before every action"
3. Done.

## Architecture Credit

Inspired by @ericosiu's "One Shared Brain" article (2026-02-10).
Same inode. Same file. N agents = N connections.
