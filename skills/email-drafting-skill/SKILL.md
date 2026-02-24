# Email Drafting Skill

## Purpose
Draft emails for Jason to review and send. NEVER send directly to clients/contacts.

## Rules
1. **ALWAYS** send drafts to jason@crossfitblaze.com first
2. **NEVER** send directly to clients, leads, or contacts
3. Jason sends from his own email after review
4. Exception: Internal system emails (backups, alerts) 

## Usage
```
# Draft reply to lead
email-draft --to "lead@example.com" --subject "Re: inquiry" --body "..."

# Send draft to Jason for review
email-send --to "jason@crossfitblaze.com" --draft-ref <id>
```

## Commands
- `email-draft` - Create email draft, save locally
- `email-send` - Send email (restricted to Jason only per rule)
- `email-list-drafts` - Show pending drafts

## Safety
- All sends logged
- Client sends blocked automatically
- Only jason@crossfitblaze.com allowed as recipient for sends
