#!/bin/bash
#
# Email Send Script - Internal Use Only
# Can send to Jason for review
# BLOCKED from sending to clients/contacts

TO="$1"
SUBJECT="$2"
BODY="$3"
FROM="daneel@aimissioncontrol.us"

# Safety check - only allow sends to Jason
if [[ "$TO" != "jason@crossfitblaze.com" ]]; then
    echo "❌ BLOCKED: Can only send to jason@crossfitblaze.com"
    echo "Draft saved locally for your review."
    echo "TO: $TO"
    echo "SUBJECT: $SUBJECT"
    echo "BODY: $BODY"
    exit 1
fi

# Send via Himalaya
himalaya message send --account Daneel "To: $TO
From: $FROM
Subject: $SUBJECT

$BODY" 2>&1

echo "✅ Email sent to $TO"
