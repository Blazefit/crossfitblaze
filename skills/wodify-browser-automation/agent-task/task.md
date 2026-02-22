# Wodify Automation Fix - Overnight Task

## Goal
Fix the Wodify browser automation and extract actual membership prices.

## Current State
- Login: Working (session restored)
- Browser: Chromium via Playwright
- Account: daneel@aimissioncontrol.us (Admin access confirmed)
- Issue: Page loading timeouts, element reference errors

## Deliverables (Complete ALL)

### 1. Fix Browser Stability
- Update wodify.py to handle loading states better
- Replace `wait_for_load_state("networkidle")` with `wait_for_timeout()` + URL checks
- Add retry logic for flaky elements
- Test navigation to multiple pages

### 2. Extract Membership Prices
Navigate through Wodify and find:
- Membership plan names
- Monthly prices
- Any initiation fees
- Plan types (Unlimited, Basic, Drop-in, etc.)

Likely locations:
- /Admin/Main?q=Contracts
- /Admin/Main?q=MembershipPlans  
- /Admin/Main?q=Financial
- /Admin/Main?q=Programs

### 3. Update add-member.py
- Replace placeholder prices with actual prices
- Update membership types to match Wodify
- Test the script works end-to-end

### 4. Create Documentation
- Save actual prices to ~/.wodify/membership-prices.json
- Document where prices were found in Wodify
- Note any special instructions

## Constraints
- USE Kimi K2.5 model
- Work until complete - do not stop
- Save all progress to git
- Log all attempts in agent-task/work-log.md

## Credentials
- Email: daneel@aimissioncontrol.us
- Password: BlazeW0dify2026!
- Saved in: ~/.wodify/credentials.json

## Success Criteria
- [ ] Can log in consistently
- [ ] Can navigate to membership/pricing section
- [ ] Actual prices extracted and documented
- [ ] add-member.py updated with correct prices
- [ ] Git commit with all changes
