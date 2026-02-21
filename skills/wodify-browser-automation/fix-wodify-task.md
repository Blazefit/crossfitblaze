# Fix Wodify Automation Script

## Problem
The wodify.py script was built for ADMIN access but the account is MEMBER-level.
Admin URLs like /Admin/Clients return 403 errors.

## Task
Update wodify.py to work with MEMBER-level access:

### What members CAN do:
- Check into WODs/classes
- View workout history
- Log personal results
- View gym calendar
- Update profile

### Changes needed:
1. Update login flow (already working - 2-step)
2. Change URLs from /Admin/* to member-appropriate URLs
3. Add member functions:
   - checkin "WOD Name" - Check into a class
   - log-workout "Workout" "Result" - Log personal result
   - view-schedule - View gym schedule
   - view-history - View personal workout history
   - update-profile - Update member profile
4. Remove admin-only functions or make them gracefully fail
5. Test the fixed script

### References:
- Current script: wodify.py
- Credentials: ~/.wodify/credentials.json
- Login URL: https://app.wodify.com/SignIn/

## Deliverables:
- Updated wodify.py with member functions
- Test that login works
- Test at least 2 member functions
- Report what was changed
