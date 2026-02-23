# WODIFY Browser Automation - Flow Documentation
**For Skill Development Collaboration**

---

## FLOW 1: Deactivate Client

### Steps:
1. Navigate to client profile: `https://app.wodify.com/Admin/Main?q=ClientProfile%7CId%3D{CLIENT_ID}`
2. Click **ACTIONS** button (top right, dropdown)
3. Click **Deactivate** option from dropdown
4. Click **Deactivate Now** in confirmation dialog
5. Wait for page refresh/redirect

### Key Elements:
- ACTIONS button: Contains text "ACTIONS" with dropdown arrow
- Deactivate option: Text exactly "Deactivate"
- Confirm button: Text contains "Deactivate Now"

### Error Handling:
- "InvalidPermissions" error = Client already inactive OR system restriction
- Check if client shows "Client is inactive" alert before attempting

---

## FLOW 2: Add Membership (Free Trial)

### Steps:
1. Navigate to client profile: `https://app.wodify.com/Admin/Main?q=ClientProfile%7CId%3D{CLIENT_ID}`
2. Click **Membership & Payments** tab (if not active)
3. Click red **+ Membership** button
4. Click **Quick Add** button in modal
5. Scroll down to find membership list
6. Click radio button for **Free Trial** (3 Classes, $0)
7. Scroll down to bottom
8. Click **Create Membership** button
9. Wait for confirmation

### Key Elements:
- Membership button: Red button with "+" and "Membership" text
- Quick Add: Button in modal dialog
- Free Trial: Row with "Free Trial" text, "3 Classes", "$0"
- Create Membership: Button at bottom of modal

### Membership Types Available:
- Free Trial - 3 Classes, $0
- Blaze Punchcard x 10 sessions - 10 Classes, $165
- Blaze Basic - 8 Classes, $0
- Drop-In - 1 Class, $20-60
- (Plus various premium plans)

---

## FLOW 3: Bulk Operations (Future)

### Approach:
1. Read CSV file with client IDs
2. For each client ID:
   - Navigate to profile
   - Check current status (avoid already inactive)
   - Perform action (deactivate/add membership)
   - Log result
   - Rate limit (wait between requests)
3. Generate report of successes/failures

### CSV Format:
```csv
client_id,name,action
4755806,Elizabeth Ferguson,add-membership:free-trial
6089489,Abby Bordeaux,deactivate
```

---

## BROWSER AUTOMATION NOTES:

### Timing:
- Wait 1-2 seconds between clicks for modals to load
- Wait 3+ seconds after "Create Membership" for confirmation
- WODIFY has AJAX loading - need to wait for elements

### Session Management:
- Requires active WODIFY login
- Browser profile must preserve cookies
- May need re-authentication if session expires

### Error Patterns:
- "InvalidPermissions" = Already inactive or insufficient permissions
- "No memberships to show" = Ready for new membership
- "$0.00 balance" = No outstanding invoices

---

## COLLABORATION NOTES:

**Daneel (Me)**: Documenting flows, testing, validation
**Claude Code**: Building skill infrastructure, code architecture

**Goal**: Create reusable `wodify` CLI tool that wraps these browser flows
