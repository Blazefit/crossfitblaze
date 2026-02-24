#!/bin/bash
# Email Drafting Skill - Main Script
# Handles drafting and sending emails with safety rules

COMMAND="$1"
shift

case "$COMMAND" in
    "draft")
        # Create draft and save to file
        TO="$1"
        SUBJECT="$2"
        BODY="$3"
        DRAFT_ID="draft-$(date +%s)"
        DRAFT_FILE="/Users/daneel/.openclaw/workspace/shared-context/email-drafts/${DRAFT_ID}.txt"
        
        mkdir -p "$(dirname "$DRAFT_FILE")"
        
        cat > "$DRAFT_FILE" << EOF
TO: $TO
SUBJECT: $SUBJECT
DATE: $(date)
---
$BODY
EOF
        
        echo "Draft created: $DRAFT_ID"
        echo "File: $DRAFT_FILE"
        ;;
        
    "send")
        # Send email - RESTRICTED per EMAIL RULE
        TO="$1"
        
        # SAFETY CHECK: Only allow sending to Jason
        if [ "$TO" != "jason@crossfitblaze.com" ]; then
            echo "ERROR: Cannot send directly to $TO"
            echo "Per EMAIL RULE: Drafts must be sent to Jason@crossfitblaze.com for review"
            echo "Use: email-draft first, then email-send jason@crossfitblaze.com"
            exit 1
        fi
        
        # Read draft from file or stdin
        if [ -f "$2" ]; then
            BODY=$(cat "$2")
        else
            BODY="$2"
        fi
        
        # Send via Himalaya
        himalaya message send --account Daneel << HIMMSG
To: $TO
From: daneel@aimissioncontrol.us
Subject: DRAFT FOR REVIEW: $3

$BODY

---
This draft was prepared for your review.
Send from your jason@crossfitblaze.com email after approval.
HIMMSG
        
        if [ $? -eq 0 ]; then
            echo "Draft sent to jason@crossfitblaze.com for review"
        else
            echo "Failed to send. Check himalaya configuration."
            exit 1
        fi
        ;;
        
    "list")
        # List pending drafts
        ls -la /Users/daneel/.openclaw/workspace/shared-context/email-drafts/ 2>/dev/null || echo "No drafts found"
        ;;
        
    *)
        echo "Email Drafting Skill"
        echo ""
        echo "Commands:"
        echo "  draft <to> <subject> <body-file>  - Create draft"
        echo "  send jason@crossfitblaze.com <draft-file> <subject> - Send to Jason"
        echo "  list - Show pending drafts"
        echo ""
        echo "SAFETY: Direct sends to clients BLOCKED per EMAIL RULE"
        ;;
esac
