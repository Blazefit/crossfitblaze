# Sunday Setup Tasks - Feb 8, 2026

## 🎯 Active Tasks

### 1. Git Repository Cleanup ✅ COMPLETED
- [x] Create proper .gitignore for sensitive files
- [x] Organize untracked files into logical commits
- [x] Commit agent configuration files (AGENTS.md, MEMORY.md, etc.)
- [x] Commit business data (crossfitblaze/, data/, templates/)
- [x] Commit memory/ daily logs
- [x] Handle sensitive files (.email-alerts-jason.json)

**Result:** 4 commits pushed to repository

### 2. Email System Setup ✅ COMPLETED
- [x] Found: Google Workspace Blaze MCP server (already configured)
- [x] Gmail tools available: gmail.send, gmail.search, gmail.get
- [x] Status: Online and authenticated
- [x] Email templates created in templates/crossfitblaze-email-templates.md

**Usage:** `mcporter call google-workspace-blaze gmail.send '{"to":["email"],"subject":"Title","body":"Message"}'`

### 3. Lead Follow-up ✅ DRAFT SENT
- [x] Reviewed Julio's inquiry details
- [x] Draft email prepared (sent via Telegram below)
- [ ] Backfill 18 existing email alerts into leads system (next)

### 4. Virus Scan / Security
- [ ] Research Matchlock sandboxing tool
- [ ] Evaluate if useful for CrossFit Blaze operations
- [ ] Document security improvements

### 5. OpenWork Bounties
- [ ] Fund Solana wallet
- [ ] Submit PinchPress bounty (10K $OPENWORK)
- [ ] Submit ClawPump bounty (500 $OPENWORK)

---

## 📂 Git Organization Plan

**Commit 1: Agent Configuration**
- AGENTS.md
- BOOTSTRAP.md
- HEARTBEAT.md
- IDENTITY.md
- MEMORY.md
- SOUL.md
- TOOLS.md
- USER.md

**Commit 2: Business Data**
- crossfitblaze/
- data/
- templates/
- reports/

**Commit 3: Memory & Operations**
- memory/
- scripts/
- ai_agent_marketplace_report.md

**Commit 4: Configuration**
- schema.json
- servers.json
- email_check.py
- submit_jobs.sh

**Do Not Commit:**
- .email-alerts-jason.json (contains sensitive data)
- peptide-inventory.html (generated)
- mission-control.html (generated)
