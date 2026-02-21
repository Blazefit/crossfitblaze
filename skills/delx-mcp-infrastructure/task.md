# Delx MCP/A2A Infrastructure Build

## Goal
Build infrastructure to connect to Delx (delx.ai) via MCP (Model Context Protocol) and A2A (Agent-to-Agent) to unlock 8.4M+ $OPENWORK in blocked bounties.

## Background
- Delx API: https://api.delx.ai/v1/mcp and /v1/a2a
- Session: 5dd1a770-b8ce-4bfe-b4b0-4ad024b071ce (from MEMORY.md)
- Status: All tools FREE during campaign
- Blocked bounties: 6 jobs, 8.4M $OPENWORK

## Deliverables

### 1. MCP Client
- Python module: `delx_mcp_client.py`
- Connect to https://api.delx.ai/v1/mcp
- Handle authentication (session-based)
- Implement: heartbeat, session management, tool calling

### 2. A2A Client  
- Python module: `delx_a2a_client.py`
- Connect to https://api.delx.ai/v1/a2a
- Agent-to-agent communication protocol
- Handle: agent discovery, message passing, state sync

### 3. Integration Skill
- SKILL.md documentation
- CLI tool: `delx-agent` with commands:
  - `heartbeat` - Send heartbeat to Delx
  - `session` - Manage agent sessions
  - `tools` - List available tools
  - `submit <bounty_id>` - Submit bounty completion
- Config: ~/.delx/config.json

### 4. OpenWork Integration
- Module to bridge Delx submissions to OpenWork
- Auto-submit bounty proofs
- Track submission status

## References
- ~/.openclaw/workspace/MEMORY.md (Delx section)
- ~/.openclaw/workspace/shared-context/agent-outputs/freelance-bounty-hunt*.md

## Success Criteria
- Successfully authenticate with Delx API
- Send heartbeat and receive acknowledgment
- List available tools
- Submit at least one test bounty
