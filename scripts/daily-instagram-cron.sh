#!/bin/bash
#
# Automated Instagram Daily Poster for CrossFit Blaze
# Runs at 9 AM daily via cron

DATE=$(date +%Y-%m-%d)
DAY=$(date +%A)
WORKSPACE="/Users/daneel/.openclaw/workspace"
MEDIA_DIR="$WORKSPACE/media/inbound"
POST_SCRIPT="$WORKSPACE/scripts/post-to-instagram.js"
LOG_FILE="$WORKSPACE/shared-context/agent-outputs/instagram-daily-posts.log"

# Content themes by day
get_caption() {
    case "$DAY" in
        "Monday") echo "New week, new goals! 💪 Start strong with CrossFit Blaze. #MotivationMonday #CrossFit #BlazeFit #CapeCoral" ;;
        "Tuesday") echo "Technique Tuesday: Form first, PRs later. 🎯 #TechniqueTuesday #CrossFit #FormMatters #BlazeFit" ;;
        "Wednesday") echo "Mid-week grind! You're halfway to the weekend. 🔥 #HumpDay #CrossFit #BlazeFit #Consistency" ;;
        "Thursday") echo "Throwback to when you thought this would be easy. 😅 #ThrowbackThursday #CrossFit #Progress #BlazeFit" ;;
        "Friday") echo "Friday energy: Leave it all on the floor. 💥 #FridayFeeling #CrossFit #BlazeFit #WeekendWarrior" ;;
        "Saturday") echo "Saturday strength session. No excuses, just results. 🏋️ #SaturdayStrength #CrossFit #BlazeFit #Weekend" ;;
        "Sunday") echo "Sunday reset. Rest, recover, repeat. 🛌 #SundayReset #Recovery #CrossFit #BlazeFit" ;;
    esac
}

# Find latest media
MEDIA_FILE=$(find "$MEDIA_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -mtime -7 2>/dev/null | head -1)

if [ -z "$MEDIA_FILE" ]; then
    echo "[$DATE] ERROR: No media found" >> "$LOG_FILE"
    exit 1
fi

CAPTION=$(get_caption)

# Post to Instagram
node "$POST_SCRIPT" "$MEDIA_FILE" "$CAPTION" 2>&1 | tee -a "$LOG_FILE"

if [ $? -eq 0 ]; then
    echo "[$DATE] SUCCESS: Posted to Instagram" >> "$LOG_FILE"
else
    echo "[$DATE] FAILED: Post unsuccessful" >> "$LOG_FILE"
fi
