#!/bin/bash
# Generate fresh daily Instagram image with DATE CHECK

DATE=$(date +%Y-%m-%d)
DAY=$(date +%A)
MONTH=$(date +%m)
DAY_NUM=$(date +%d)

# CRITICAL: Check for inappropriate holiday content
if [ "$MONTH" == "02" ] && [ "$DAY_NUM" -gt "17" ]; then
    # After Feb 17, NO Valentine's content allowed
    HOLIDAY_CHECK="NO_VALENTINE"
    PROMPT="Modern CrossFit gym interior, professional fitness equipment, barbells, kettlebells, industrial lighting, motivational atmosphere, clean and organized, wide angle shot, morning light, NO people, NO hearts, NO romantic themes, just pure gym equipment and space"
elif [ "$MONTH" == "03" ] && [ "$DAY_NUM" -lt "14" ]; then
    # Before St. Patrick's Day
    HOLIDAY_CHECK="NO_ST_PATRICKS"
    PROMPT="Modern CrossFit gym interior, professional fitness equipment, barbells, kettlebells, industrial lighting, motivational atmosphere, clean and organized, NO green themes, NO shamrocks, NO holiday decorations"
else
    # Normal day
    PROMPT="Modern CrossFit gym interior, professional fitness equipment, barbells, kettlebells, industrial lighting, motivational atmosphere, clean and organized"
fi

# Generate using Pollinations.ai (free)
ENCODED_PROMPT=$(echo "$PROMPT" | sed 's/ /%20/g' | sed "s/'/%27/g")
IMAGE_URL="https://image.pollinations.ai/prompt/${ENCODED_PROMPT}?width=1080&height=1080&seed=${RANDOM}&nologo=true"

OUTPUT_FILE="media/generated/${DATE}-${DAY}.jpg"
mkdir -p media/generated

# Download with timeout
curl -s -L --max-time 30 "$IMAGE_URL" -o "$OUTPUT_FILE" 2>/dev/null

if [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
    echo "✓ Generated: $OUTPUT_FILE"
    echo "✓ Date: $DATE"
    echo "✓ Holiday check: $HOLIDAY_CHECK"
    echo "$OUTPUT_FILE"
else
    echo "✗ Generation failed, using fallback"
    # Create a simple colored background with text using ImageMagick if available
    echo "fallback"
fi
