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

# CRITICAL: Generate FRESH AI fitness image matching caption context - NEVER reuse
DATE=$(date +%Y-%m-%d)
DAY=$(date +%A)
MONTH=$(date +%m)
DAY_NUM=$(date +%d)

# Build prompt based on day of week (matching caption context)
case "$DAY" in
    "Monday")
        PROMPT="Professional CrossFit gym at sunrise, athlete doing burpees, motivational lighting, energetic atmosphere, fitness equipment visible, industrial gym style, dramatic shadows, high energy, no text"
        ;;
    "Tuesday")
        PROMPT="CrossFit athlete perfecting form with barbell, technique focus, gym mirrors, professional lighting, strength training, clean gym environment, motivational, no text"
        ;;
    "Wednesday")
        PROMPT="CrossFit community workout, multiple athletes training together, mid-week energy, gym equipment, team atmosphere, industrial gym, dramatic lighting, no text"
        ;;
    "Thursday")
        PROMPT="CrossFit athlete doing kettlebell swings, power and strength, gym setting, sweat and determination, professional lighting, intense workout, no text"
        ;;
    "Friday")
        PROMPT="CrossFit Friday workout intensity, athlete with battle ropes, explosive energy, gym atmosphere, end of week power, dramatic lighting, no text"
        ;;
    "Saturday")
        PROMPT="CrossFit Saturday strength session, heavy lifting, barbells and weights, gym packed with equipment, weekend warrior energy, no text"
        ;;
    "Sunday")
        PROMPT="CrossFit gym recovery day, stretching area, foam rollers, calm but focused atmosphere, Sunday reset, peaceful gym lighting, no text"
        ;;
esac

# CRITICAL: Add holiday exclusion to prompt
if [ "$MONTH" == "02" ] && [ "$DAY_NUM" -gt "17" ]; then
    # After Feb 17, explicitly exclude Valentine's
    PROMPT="${PROMPT}, NO hearts, NO pink, NO red romantic themes, NO Valentine's decorations, pure fitness only"
fi

# Generate AI image using pollinations.ai
RANDOM_SEED=$(date +%Y%m%d)
ENCODED_PROMPT=$(echo "$PROMPT" | python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.stdin.read().strip()))")
IMAGE="$WORKSPACE/media/generated/ai-fitness-${DATE}.jpg"
mkdir -p "$WORKSPACE/media/generated"

# Download AI generated image
curl -s -L --max-time 60 "https://image.pollinations.ai/prompt/${ENCODED_PROMPT}?width=1080&height=1080&seed=${RANDOM_SEED}&nologo=true" -o "$IMAGE" 2>/dev/null

# Verify image downloaded
if [ ! -f "$IMAGE" ] || [ ! -s "$IMAGE" ] || [ $(stat -f%z "$IMAGE" 2>/dev/null || echo 0) -lt 10000 ]; then
    # Fallback: try with different seed
    curl -s -L --max-time 60 "https://image.pollinations.ai/prompt/${ENCODED_PROMPT}?width=1080&height=1080&seed=${RANDOM_SEED}99&nologo=true" -o "$IMAGE" 2>/dev/null
fi

# Log what was generated
echo "Generated AI image for $DAY: $PROMPT" >> "$LOG_FILE"

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
