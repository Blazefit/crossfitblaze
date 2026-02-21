#!/usr/bin/env python3
"""
Instagram Post Automation via upload-post API
Posts images with captions to @crossfitblaze Instagram account

Usage: python3 post-to-instagram.py <image_path> <caption> [--dry-run]
Example: python3 post-to-instagram.py ./image.jpg "Great workout! #CrossFit"
"""

import sys
import os
import json
import requests
from pathlib import Path
from datetime import datetime

# Configuration
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImNvc2RhbmVlbG9saXZhd0BnbWFpbC5jb20iLCJleHAiOjQ5MjQ0MjA2MTIsImp0aSI6IjM0YThjZmU1LWY1NDEtNGUwZC1hZDI0LTNlNGMwMWI5YzRiOSJ9.DC0JGSRvMMnk5oBLPaNNS9-FzMIP2kKdOWuRBmjciKU'
API_BASE = 'https://api.upload-post.com'
UPLOAD_ENDPOINT = '/api/upload_photos'
USERNAME = 'crossfitblaze'


def post_to_instagram(image_path, caption, dry_run=False):
    """
    Post image with caption to Instagram via upload-post API

    Args:
        image_path: Path to image file
        caption: Instagram post caption
        dry_run: If True, don't actually post

    Returns:
        dict: Response data with success status and post details
    """
    # Validate inputs
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if not caption or not caption.strip():
        raise ValueError("Caption is required")

    if dry_run:
        print("🔍 DRY RUN MODE - No actual post will be made")
        print(f"Image: {image_path}")
        print(f"Caption: {caption}")
        print(f"Platform: Instagram (@crossfitblaze)")
        return {
            'success': True,
            'dry_run': True,
            'message': 'Dry run completed successfully'
        }

    # Prepare request
    url = f"{API_BASE}{UPLOAD_ENDPOINT}"
    headers = {
        'Authorization': f'Apikey {API_KEY}'
    }

    # Get first line of caption as title
    title = caption.split('\n')[0][:100]

    # Prepare multipart form data
    files = {
        'photos[]': (os.path.basename(image_path), open(image_path, 'rb'), 'image/jpeg')
    }

    data = {
        'user': USERNAME,
        'platform[]': 'instagram',
        'title': title,
        'description': caption
    }

    print("📤 Uploading to Instagram...")
    print(f"Image: {os.path.basename(image_path)}")
    print(f"Caption length: {len(caption)} characters")

    # Make request
    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        print(f"Response status: {response.status_code}")

        response_data = response.json()

        if response.status_code >= 200 and response.status_code < 300:
            print("✅ Post successful!")
            return {
                'success': True,
                'status_code': response.status_code,
                'data': response_data
            }
        else:
            print("❌ Post failed")
            print(f"Response: {response.text}")
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {str(e)}")
        raise
    finally:
        # Close file handle
        if 'photos[]' in files:
            files['photos[]'][1].close()


def main():
    """Main execution"""
    args = sys.argv[1:]

    if len(args) < 2 or '--help' in args or '-h' in args:
        print("Usage: python3 post-to-instagram.py <image_path> <caption> [--dry-run]")
        print("")
        print("Arguments:")
        print("  image_path    Path to image file (jpg, jpeg, png)")
        print("  caption       Instagram post caption")
        print("  --dry-run     Test without actually posting")
        print("")
        print("Example:")
        print('  python3 post-to-instagram.py ./workout.jpg "Great session! 💪 #CrossFit"')
        sys.exit(0 if ('--help' in args or '-h' in args) else 1)

    image_path = os.path.abspath(args[0])
    caption = args[1]
    dry_run = '--dry-run' in args

    print("=== CrossFit Blaze Instagram Post ===")
    print("Account: @crossfitblaze")
    print("")

    try:
        result = post_to_instagram(image_path, caption, dry_run)

        if result['success']:
            print("")
            print("📊 Result:")
            print(json.dumps(result, indent=2))

            if not dry_run and 'data' in result:
                # Log success to file
                log_dir = '/Users/daneel/.openclaw/workspace/shared-context/agent-outputs'
                log_file = os.path.join(log_dir, f"instagram-post-{datetime.now().strftime('%Y-%m-%d')}.log")
                log_entry = f"[{datetime.now().isoformat()}] SUCCESS: {os.path.basename(image_path)}\n{caption}\n---\n"
                with open(log_file, 'a') as f:
                    f.write(log_entry)

            sys.exit(0)

    except Exception as e:
        print("")
        print(f"💥 Error: {str(e)}")

        # Log error to file
        log_dir = '/Users/daneel/.openclaw/workspace/shared-context/agent-outputs'
        error_file = os.path.join(log_dir, f"instagram-post-errors-{datetime.now().strftime('%Y-%m-%d')}.log")
        error_entry = f"[{datetime.now().isoformat()}] ERROR: {str(e)}\nImage: {image_path}\n---\n"
        with open(error_file, 'a') as f:
            f.write(error_entry)

        sys.exit(1)


if __name__ == '__main__':
    main()
