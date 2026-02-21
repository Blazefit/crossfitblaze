#!/bin/bash

# Job Tracker Update Script
TRACKER_FILE="/Users/daneel/.openclaw/workspace/memory/job_tracker.md"

# Function to add a new job
add_job() {
    local job_id="$1"
    local job_title="$2"
    local reward="$3"
    local status="${4:-Submitted}"

    echo "### New Job Entry: $(date '+%Y-%m-%d %H:%M:%S')" >> "$TRACKER_FILE"
    echo "- Job ID: $job_id" >> "$TRACKER_FILE"
    echo "- Title: $job_title" >> "$TRACKER_FILE"
    echo "- Reward: $reward tokens" >> "$TRACKER_FILE"
    echo "- Status: $status" >> "$TRACKER_FILE"
    echo "- Payment: Pending ⏳" >> "$TRACKER_FILE"
    echo "" >> "$TRACKER_FILE"
}

# Function to update job status
update_job_status() {
    local job_id="$1"
    local new_status="$2"
    local payment_status="${3:-Pending}"

    sed -i '' "/$job_id/,/^$/c\### Job Update: $(date '+%Y-%m-%d %H:%M:%S')\n- Job ID: $job_id\n- Status: $new_status\n- Payment: $payment_status\n" "$TRACKER_FILE"
}

# Main logic
case "$1" in
    "add")
        add_job "$2" "$3" "$4" "$5"
        ;;
    "update")
        update_job_status "$2" "$3" "$4"
        ;;
    *)
        echo "Usage: $0 {add|update} [parameters]"
        exit 1
        ;;
esac