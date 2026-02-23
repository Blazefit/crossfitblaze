# Wodify Protocol - Quick Reference
**CrossFit Blaze Internal Documentation**

---

## 🚨 CRITICAL: Use browser-use, NOT Native Browser

For all Wodify operations, use the `browser-use` CLI with `--headed` flag:

```bash
browser-use --headed open "https://app.wodify.com/Admin/"
```

The OpenClaw native browser tool **cannot** handle JavaScript-heavy Wodify pages.

---

## 🔑 Login Credentials (DO NOT SHARE)

- **Email:** daneel@aimissioncontrol.us
- **Password:** BlazeW0dify2026!
- **MFA:** Email-based (check Zoho Mail)
- **Session:** Trusted for 90 days after login

---

## 📋 Working Commands

### 1. Outstanding Invoices

**Quick Check:**
```bash
browser-use --headed open "https://app.wodify.com/Admin/Main?q=AgedReceivables"
```

**Current Outstanding (as of 2026-02-23):**

| Member | Invoice # | Status |
|--------|-----------|--------|
| Michele Horman | 00022654 | Unpaid |
| daniela sanchez | 00022657 | Unpaid |
| Jonathan Vega | 00022682 | Unpaid |
| Tom Wooden | 00022705 | Unpaid |

### 2. Attendance Reports

**Access Reports:**
```bash
browser-use --headed open "https://app.wodify.com/Admin/Main?q=AnalyticsDashboard"
```

**Available Reports:**
- ✅ **Attendance Trend** - Weekly averages (last 4 weeks vs previous 4)
- ✅ **Weekly Attendance Streaks** - Current/highest streaks
- ✅ **Most Recent Attendance** - Recent check-ins
- ⚠️ **Total 2026 Attendance** - Not directly available; requires export

### 3. Member Management

**Search Member:**
```bash
browser-use --headed open "https://app.wodify.com/Admin/Main?q=ClientSearch"
browser-use state  # Get search input index
browser-use input <index> "Member Name"
```

**Navigate Profile:**
```bash
browser-use click <member-name-link>
```

### 4. Today's Schedule

```bash
browser-use --headed open "https://app.wodify.com/Admin/Main?q=WeekWorkouts"
browser-use click <today-button>
```

---

## 🗺️ Menu Navigation

Open hamburger menu [ref=e10] for full navigation:

```
Financial → Invoices → [Unpaid this Month / Overdue]
Analytics → Reports → Attendance → [Attendance Trend]
People → Client Search
Classes → Schedule
```

---

## 🛠️ Troubleshooting

**Page Blank?**
```bash
browser-use wait selector "table" --timeout 10000
browser-use scroll down
```

**Session Expired?**
```bash
browser-use close --all
# Re-run login flow
```

**Can't Find Element?**
```bash
browser-use state | grep "Text to Find" -B5
```

**Check Email for MFA Code:**
```bash
himalaya envelope list --folder INBOX
himalaya message read <email-id>
```

---

## 📸 Screenshots

Recent screenshots saved:
- `/tmp/wodify-unpaid-invoices.png` - Outstanding invoices
- `/tmp/wodify-attendance-trend.png` - Attendance report
- `/tmp/wodify-weekly-streaks.png` - Streaks report

---

## 📝 Notes

- **MFA Required:** Yes, on every new session
- **Session Persistence:** 90 days with "Trust this device"
- **Report Loading:** 3-5 seconds for data tables
- **Metabase Reports:** Load in iframe; may need scrolling
- **Best Time to Check:** Business hours (Wodify server responsive)

---

## 🚀 Automation Ideas

### Daily (Cron Job)
```
6:00 AM - Check overnight leads
6:30 AM - Verify today's WOD is posted
7:00 AM - Check class rosters for low attendance
```

### Weekly (Cron Job)
```
Monday 8:00 AM - Generate unpaid invoices report
Tuesday 9:00 AM - Attendance trend analysis
Friday 5:00 PM - Upcoming expirations check
```

### Ad-Hoc Triggers
```
- New lead notification → Immediate follow-up
- Class cancellation → Notify members
- Failed payment → Payment reminder
```

---

## ⚠️ Privacy & Security

- **Never share** login credentials in group chats
- **Never post** member financial details publicly
- **Always use** private messages for sensitive data
- **Screenshots** may contain PII - store securely
- **Log all changes** for audit trail

---

## 📞 Escalation

If Wodify automation fails:
1. Check `browser-use doctor`
2. Verify network connectivity
3. Clear browser cache: `browser-use close --all`
4. Contact: Jason (jason@crossfitblaze.com)

---

**Document Version:** 1.0
**Last Updated:** 2026-02-23
**Maintained By:** Daneel
