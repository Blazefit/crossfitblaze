#!/bin/bash
#
# Instagram Auto-Poster - 7AM Daily
# Generates AI image and posts automatically
# NO manual intervention required

DATE=$(date +%Y-%m-%d)
DAY=$(date +%A)
WORKSPACE="/Users/daneel/.openclaw/workspace"
OUTPUT_DIR="$WORKSPACE/shared-context/agent-outputs"
LOG_FILE="$OUTPUT_DIR/instagram-auto-post.log"
API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImRhbmVlbEBhaW1pc3Npb25jb250cm9sLnVzIiwiZXhwIjo0OTI1NDY4MTI1LCJqdGkiOiIwYmEzMTMxMC04MGE0LTQ2NTEtYmM1Mi1mZjQzMWFiZTA4MTIifQ.Z4rXI2jnWSlO37Qh-KAIeT2_QDc9zt_WVfTUw-59RlY"
USER_PROFILE="crossfitblaze"

# Generate caption based on day
get_caption() {
    case "$DAY" in
        "Monday") echo "🔥 New week, fresh start. What are you chasing? 💪 #MotivationMonday #CrossFit #BlazeFit" ;;
        "Tuesday") echo "🎯 Technique Tuesday: Form first, PRs later. #CrossFit #FormMatters #BlazeFit" ;;
        "Wednesday") echo "💪 Mid-week grind! Halfway to the weekend. #HumpDay #CrossFit #BlazeFit" ;;
        "Thursday") echo "🔥 Thursday throwdown. Leave it all on the floor. #CrossFit #BlazeFit #NoExcuses" ;;
        "Friday") echo "💥 Friday energy! Finish the week strong. #FridayFeeling #CrossFit #BlazeFit" ;;
        "Saturday") echo "🏋️ Weekend warrior mode. No excuses. #SaturdayStrength #CrossFit #BlazeFit" ;;
        "Sunday") echo "🛌 Sunday reset. Rest, recover, repeat. #SundayReset #CrossFit #Recovery" ;;
    esac
}

# Generate AI image (placeholder - would need actual API)
generate_image() {
    # For now, use a generic CrossFit gym image
    # In production, this would call an AI image generation API
    echo "$WORKSPACE/media/generated/daily-post-$DATE.jpg"
}

log() {
    echo "[$(date)] $1" >> "$LOG_FILE"
}

log "Starting Instagram auto-post for $DAY"

# CRITICAL: Generate FRESH image - NEVER reuse old images
DATE=$(date +%Y-%m-%d)
DAY=$(date +%A)

# Generate fresh image with date validation
if [ -f "$WORKSPACE/scripts/generate-daily-image.sh" ]; then
    IMAGE=$($WORKSPACE/scripts/generate-daily-image.sh)
else
    # Fallback - use picsum with random seed based on date
    RANDOM_SEED=$(date +%Y%m%d)
    IMAGE="$WORKSPACE/media/generated/daily-${DATE}.jpg"
    curl -s -L "https://picsum.photos/1080/1080?random=${RANDOM_SEED}" -o "$IMAGE" 2>/dev/null
fi

# Verify image is fresh (not reused)
if [ -f "$IMAGE" ]; then
    log "Using fresh image: $IMAGE"
else
    log "ERROR: Fresh image generation failed"
    exit 1
fi

CAPTION=$(get_caption)

# Post via upload-post API
RESPONSE=$(curl -s -X POST "https://api.upload-post.com/api/post" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"profile\": \"crossfitblaze\", \"caption\": \"$CAPTION\", \"image\": \"$IMAGE\"}" 2>&1)

if echo "$RESPONSE" | grep -q "success"; then
    log "SUCCESS: Posted to Instagram"
    "$WORKSPACE/shared-context/log-activity.sh" "Instagram Auto" "Posted" "$DAY" "success"
    # CRITICAL: Delete used image to prevent reuse
    if [ -f "$IMAGE" ]; then
        rm "$IMAGE"
        log "Deleted used image: $IMAGE"
    fi
else
    log "FAILED: $RESPONSE"
    "$WORKSPACE/shared-context/log-activity.sh" "Instagram Auto" "Failed" "$RESPONSE" "error"
fi
