#!/usr/bin/env bash
#
# Autonomous Instagram Posting System for CrossFit Blaze
# This script runs daily at 9 AM to post content automatically
# No human intervention required

set -e

API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImNvc2RhbmVlbG9saXZhd0BnbWFpbC5jb20iLCJleHAiOjQ5MjQ0MjA2MTIsImp0aSI6IjM0YThjZmU1LWY1NDEtNGUwZC1hZDI0LTNlNGMwMWI5YzRiOSJ9.DC0JGSRvMMnk5oBLPaNNS9-FzMIP2kKdOWuRBmjciKU"
API_BASE="https://api.upload-post.com/api"
WORKSPACE="/Users/daneel/.openclaw/workspace"
MEDIA_DIR="$WORKSPACE/media/inbound"
OUTPUT_DIR="$WORKSPACE/shared-context/agent-outputs"
DATE=$(date +%Y-%m-%d)
DAY_OF_WEEK=$(date +%A)

# Content templates by day
get_content_plan() {
    case "$DAY_OF_WEEK" in
        "Monday")
            echo "Motivation Monday - New week, fresh start"
            ;;
        "Tuesday")
            echo "Technique Tuesday - Form focus"
            ;;
        "Wednesday")
            echo "Member Spotlight - Success stories"
            ;;
        "Thursday")
            echo "Throwback Thursday - Classic moments"
            ;;
        "Friday")
            echo "Feature Friday - Equipment or movement"
            ;;
        "Saturday")
            echo "Saturday Strength - Weekend warrior"
            ;;
        "Sunday")
            echo "Sunday Reset - Rest and recovery"
            ;;
    esac
}

# Check for available media
check_media() {
    # Look for recent media files (last 7 days)
    find "$MEDIA_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.mp4" \) \
        -mtime -7 2>/dev/null | head -5
}

# Generate caption based on content type
generate_caption() {
    local content_type="$1"
    
    case "$content_type" in
        "Motivation Monday")
            cat << 'EOF'
New week. Same standards. 💪

Monday sets the tone. Show up anyway.

#CrossFit #MondayMotivation #BlazeFit #CapeCoral #Fitness #NewWeek
EOF
            ;;
        "Technique Tuesday")
            cat << 'EOF'
Form first. Always. 🔧

Good movement = better results + fewer injuries.

What's your biggest form struggle? Drop it below 👇

#CrossFit #TechniqueTuesday #FormMatters #BlazeFit
EOF
            ;;
        "Member Spotlight")
            cat << 'EOF'
Consistency compounds. 📈

30 days of showing up changes everything.

#CrossFit #Transformation #Consistency #BlazeFit #CapeCoral
EOF
            ;;
        "Saturday Strength")
            cat << 'EOF'
Weekend warriors. 🔥

Saturday hits different when you're here.

#CrossFit #Saturday #WeekendWarrior #BlazeFit
EOF
            ;;
        *)
            cat << 'EOF'
Blaze Fit. Every day. 💪

#CrossFit #BlazeFit #CapeCoral #Fitness
EOF
            ;;
    esac
}

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$OUTPUT_DIR/instagram-auto-post.log"
}

# Main execution
main() {
    log "=== Starting autonomous Instagram post ==="
    log "Day: $DAY_OF_WEEK ($DATE)"
    
    # Get today's content plan
    CONTENT_PLAN=$(get_content_plan)
    log "Content plan: $CONTENT_PLAN"
    
    # Check for media
    MEDIA_FILES=$(check_media)
    MEDIA_COUNT=$(echo "$MEDIA_FILES" | wc -l)
    
    if [ -n "$MEDIA_FILES" ] && [ "$MEDIA_COUNT" -gt 0 ]; then
        log "Found $MEDIA_COUNT media files"
        SELECTED_MEDIA=$(echo "$MEDIA_FILES" | head -1)
        log "Selected: $SELECTED_MEDIA"
    else
        log "⚠️ No media found in inbound folder"
        log "Creating text-only post or using fallback"
        # TODO: Implement Canva API or stock image integration
        # For now, we'll log and skip
        echo "NO_MEDIA_AVAILABLE" > "$OUTPUT_DIR/instagram-post-$DATE.status"
        log "Status: FAILED - No media available"
        exit 1
    fi
    
    # Generate caption
    CAPTION=$(generate_caption "$CONTENT_PLAN")
    log "Caption generated"

    # Post to Instagram via upload-post API
    log "Posting to Instagram..."

    POST_RESULT=$(node "$WORKSPACE/scripts/post-to-instagram.js" "$SELECTED_MEDIA" "$CAPTION" 2>&1)
    POST_EXIT_CODE=$?

    if [ $POST_EXIT_CODE -eq 0 ]; then
        log "✅ Instagram post successful!"

        # Extract post URL from result
        POST_URL=$(echo "$POST_RESULT" | grep -o 'https://www.instagram.com/p/[^"]*' | head -1)

        cat > "$OUTPUT_DIR/instagram-post-$DATE.md" << EOF
# Instagram Post - SUCCESS

**Date:** $DATE
**Day:** $DAY_OF_WEEK
**Status:** ✅ POSTED

## Post Details
**URL:** $POST_URL
**Media:** $SELECTED_MEDIA

## Caption
$CAPTION

## API Response
\`\`\`
$POST_RESULT
\`\`\`

---
Posted: $(date)
EOF
        log "Post details saved to instagram-post-$DATE.md"
        exit 0
    else
        log "❌ Instagram post failed"
        log "Error: $POST_RESULT"

        # Create fallback task for manual review
        cat > "$OUTPUT_DIR/instagram-post-ready-$DATE.md" << EOF
# Instagram Post Ready for Review

**Date:** $DATE
**Day:** $DAY_OF_WEEK
**Status:** PENDING_REVIEW

## Content
**Type:** $CONTENT_PLAN
**Media:** $SELECTED_MEDIA

## Caption
$CAPTION

## Action Required
Spark to upload via upload-post dashboard

## Auto-Post Status
❌ API call failed - manual upload required

## Error Details
\`\`\`
$POST_RESULT
\`\`\`

---
Generated: $(date)
EOF

        log "Post ready file created: instagram-post-ready-$DATE.md"
        log "Status: FAILED - Manual intervention required"
        exit 1
    fi
}

main "$@"
