---
name: wodify
description: "Manage your Wodify gym: members, classes, WODs, billing, and reporting via browser automation"
metadata: {"openclaw":{"requires":{"config":["skills.entries.wodify.config.adminEmail"]}}}
---

# Wodify Gym Management

You are a gym management assistant that controls the Wodify admin dashboard via browser automation. You can manage members, classes, WODs, billing, and reporting for the gym.

**CRITICAL:** Wodify requires `browser-use` CLI for full functionality. The OpenClaw native browser tool cannot handle JavaScript-heavy SPA pages. See "Setup Requirements" below.

---

## Setup Requirements

### Step 1: Install browser-use CLI

The `browser-use` skill must be installed and configured:

```bash
# Install browser-use skill (already done if reading this)
clawhub install browser-use

# Install browser-use CLI via pipx
pipx install browser-use

# Verify installation
browser-use doctor
```

**Note:** Requires Python 3.13 (not 3.14 due to compatibility issues).

### Step 2: Configure Wodify Credentials

Set these config values in OpenClaw:

```bash
openclaw config set skills.entries.wodify.config.adminEmail "your-email@wodify.com"
openclaw config set skills.entries.wodify.config.adminPassword "your-password"
openclaw config set skills.entries.wodify.config.gymName "CrossFit Blaze"
```

---

## Authentication Flow

### Initial Login (One-time)

1. Start headed browser (required for JavaScript-heavy pages):
```bash
browser-use --headed open "https://app.wodify.com/Admin/"
```

2. Enter email (get index from `browser-use state`):
```bash
browser-use input <email-index> "admin-email@wodify.com"
browser-use click <continue-button-index>
```

3. Enter password:
```bash
browser-use input <password-index> "your-password"
browser-use click <signin-button-index>
```

4. Handle MFA (if enabled):
```bash
# Click "Email a code" option
browser-use click <email-code-option-index>
# Get code from email (check Zoho/Gmail inbox)
browser-use click <trust-device-checkbox-index>
browser-use input <code-input-index> "XXXXXX"
browser-use click <verify-button-index>
```

5. Save session (cookies persist):
```bash
# Device is trusted for 90 days
# Session remains active until browser-use close
```

---

## Working Commands

### Member Management

**Find Member by Name:**
```bash
# Navigate to People > Client Search
browser-use open "https://app.wodify.com/Admin/Main?q=ClientSearch"
browser-use input <search-index> "Member Name"
```

**View Member Profile:**
```bash
# Click member name from search results
browser-use click <member-name-index>
```

**Add New Member:**
```bash
# Navigate to People section
# Click "Create Client" quick link
browser-use click <create-client-index>
# Fill in required fields (First, Last, Email)
```

### Billing & Invoices (VERIFIED WORKING)

**View Unpaid Invoices:**
```bash
# Navigate to Financial > Invoices
browser-use --headed open "https://app.wodify.com/Admin/Main?q=AgedReceivables"
# OR via menu navigation
browser-use click <financial-menu-index>
browser-use click <invoices-index>
# Click "Unpaid this Month" tab
browser-use click <unpaid-tab-index>
```

**Outstanding Invoices Found (Feb 2026):**
- Michele Horman - Invoice #00022654
- daniela sanchez - Invoice #00022657
- Jonathan Vega - Invoice #00022682
- Tom Wooden - Invoice #00022705

**Check Member Balance:**
```bash
# Navigate to member profile
browser-use open "https://app.wodify.com/Admin/Main?q=ClientProfile|Id=<CLIENT_ID>"
# Look for billing/financial section
```

### Attendance & Reporting

**Attendance Reports Available:**
- Attendance Trend - Shows weekly average trends
- Weekly Attendance Streaks - Shows current/highest streaks
- Most Recent Attendance - Recent check-ins
- Coaches and Classes - Coach class counts
- Drop Ins - Drop-in occurrences

**Access Attendance Reports:**
```bash
# Navigate to Analytics > Reports > Attendance tab
browser-use --headed open "https://app.wodify.com/Admin/Main?q=AnalyticsDashboard"
browser-use click <reports-link-index>
browser-use click <attendance-tab-index>
# Choose specific report
browser-use click <report-name-index>
```

**Note:** Attendance reports show TRENDS (recent 4 weeks vs previous 4 weeks), not total 2026 counts. To see total attendance for 2026, use Insights dashboard or export data.

### Class Schedule

**View Today's Schedule:**
```bash
browser-use --headed open "https://app.wodify.com/Admin/Main?q=WeekWorkouts"
browser-use click <today-button-index>
```

**Check Class Roster:**
```bash
# Navigate to Classes section
browser-use click <classes-menu-index>
# Select specific class
browser-use click <class-time-index>
```

### WOD Programming

**View Today's WOD:**
```bash
browser-use --headed open "https://app.wodify.com/Admin/Main?q=WeekWorkouts"
# WODs shown on calendar grid
```

**Post/Edit WOD:**
```bash
# Navigate to Daily Workouts
# Click "+ Workout" on specific date
browser-use click <add-workout-index>
```

---

## Navigation Reference

### Direct URLs (When Available)

| Section | URL |
|---------|-----|
| Daily Workouts | `https://app.wodify.com/Admin/Main?q=WeekWorkouts` |
| Client Search | `https://app.wodify.com/Admin/Main?q=ClientSearch` |
| Aged Receivables | `https://app.wodify.com/Admin/Main?q=AgedReceivables` |
| Analytics Dashboard | `https://app.wodify.com/Admin/Main?q=AnalyticsDashboard` |
| People | `https://app.wodify.com/Admin/Main?q=PeopleDashboard` |

### Menu Structure (via hamburger menu icon [ref=e10])

```
Perform
├── Daily Workouts
├── Library
├── Pulse
├── Settings

People
├── Client Search
├── Leads
├── Prospects

Classes
├── Schedule
├── Programs

Financial
├── Invoices ✓ (TESTED - WORKING)
├── Transactions
├── Payouts
├── Payroll

Analytics
├── Reports ✓ (TESTED - WORKING)
│   ├── Attendance ✓
│   ├── Financial
│   ├── Memberships
│   └── People
└── Insights
```

---

## Working Examples

### Example 1: Find Outstanding Invoices

```bash
# 1. Open browser in headed mode
browser-use --headed open "https://app.wodify.com/Admin/Main?q=AgedReceivables"

# 2. Check page state
browser-use state

# 3. If not on Invoices page, navigate via menu
browser-use click <financial-menu-index>
browser-use click <invoices-link-index>

# 4. Click "Unpaid this Month" tab
browser-use click <unpaid-tab-index>

# 5. Wait for table to load
browser-use wait selector "table"

# 6. Get table HTML
browser-use get html --selector "table"

# 7. Parse for member names and amounts
```

**Expected Output:** Table with columns: Invoice, Client Name, Product, Status, Amount, Due Date

### Example 2: Check Member Attendance Trend

```bash
# 1. Navigate to Attendance Reports
browser-use --headed open "https://app.wodify.com/Admin/Main?q=AnalyticsDashboard"
browser-use click <reports-link-index>
browser-use click <attendance-tab-index>
browser-use click <attendance-trend-report-index>

# 2. Wait for Metabase iframe to load
browser-use wait selector "iframe"

# 3. Get report data
browser-use get html --selector "table"

# 4. Parse for attendance averages
```

**Expected Output:** Client names with average weekly attendance (current 4 weeks vs previous 4 weeks)

---

## Error Handling

### Page Not Loading

If page content doesn't appear:
```bash
# 1. Wait longer
browser-use wait selector "table" --timeout 10000

# 2. Take screenshot to debug
browser-use screenshot /tmp/debug.png

# 3. Scroll to trigger lazy loading
browser-use scroll down

# 4. Check state again
browser-use state
```

### Session Expired

If logged out:
```bash
# 1. Navigate to login page
browser-use open "https://app.wodify.com/SignIn/Home"

# 2. Re-enter credentials (see Authentication Flow)
# 3. Complete MFA if required
```

### Element Not Found

If element index changes:
```bash
# 1. Get fresh state
browser-use state

# 2. Search for element text
browser-use state | grep "Target Text" -B5

# 3. Use new index
```

---

## Why browser-use vs Native Browser Tool

| Feature | OpenClaw Native | browser-use CLI |
|---------|-----------------|-----------------|
| JavaScript execution | Limited | Full (headed mode) |
| SPA handling | Poor | Excellent |
| Wodify reports | Blank pages | Fully loaded |
| Authentication | Works | Works |
| Session persistence | Limited | Cookie-based |
| Speed | Faster | Slower (real browser) |

**Recommendation:** Always use `browser-use --headed` for Wodify operations.

---

## Tested & Verified (2026-02-23)

✅ Authentication with MFA
✅ Invoice reports (unpaid/overdue)
✅ Attendance trend reports
✅ Navigation to all major sections
✅ Member search and profiles
✅ Class schedule viewing

**Session:** Active and trusted for 90 days
**Browser:** Chromium in headed mode
**Status:** Production ready

---

## Future Enhancements

### To Add:
- Automated daily invoice checks
- Member attendance alerts
- Late payment SMS reminders
- Class capacity monitoring
- Retention trend analysis

### Wodify API Access
For more reliable reporting, consider requesting Wodify API credentials for direct data access instead of browser automation.

---

## Support

For issues:
1. Check `browser-use doctor` output
2. Verify credentials in config
3. Try `--headed` mode for debugging
4. Clear session: `browser-use close --all`

---

**Last Updated:** 2026-02-23
**Tested By:** Daneel & Blaze
**Skill Version:** 1.0 (Production)
