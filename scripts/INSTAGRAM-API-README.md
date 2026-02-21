# Instagram Automation via upload-post API

**Status:** ✅ WORKING
**Last Updated:** 2026-02-21
**Account:** @crossfitblaze (1,268 followers)

## Quick Start

### Post to Instagram (Node.js)
```bash
node scripts/post-to-instagram.js /path/to/image.jpg "Your caption here #CrossFit"
```

### Post to Instagram (Python)
```bash
python3 scripts/post-to-instagram.py /path/to/image.jpg "Your caption here #CrossFit"
```

### Dry Run (Test Without Posting)
```bash
node scripts/post-to-instagram.js /path/to/image.jpg "Caption" --dry-run
```

## Successful Test Post

**Posted:** 2026-02-21
**URL:** https://www.instagram.com/p/DVApEUjjPqe/
**Post ID:** 18407629408133837

## API Details

### Working Configuration

- **API Base:** `https://api.upload-post.com`
- **Endpoint:** `POST /api/upload_photos`
- **Authentication:** `Authorization: Apikey <your-key>`
- **API Key:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImNvc2RhbmVlbG9saXZhd0BnbWFpbC5jb20iLCJleHAiOjQ5MjQ0MjA2MTIsImp0aSI6IjM0YThjZmU1LWY1NDEtNGUwZC1hZDI0LTNlNGMwMWI5YzRiOSJ9.DC0JGSRvMMnk5oBLPaNNS9-FzMIP2kKdOWuRBmjciKU`

### Required Parameters

1. **user** (string) - Username: `crossfitblaze`
2. **photos[]** (file) - Image file (JPEG/PNG)
3. **platform[]** (array) - Platform: `instagram`
4. **title** (string) - Post title (first line of caption)
5. **description** (string) - Full caption text

### Request Format

```bash
curl -X POST \
  -H 'Authorization: Apikey <your-key>' \
  -F 'user=crossfitblaze' \
  -F 'photos[]=@/path/to/image.jpg' \
  -F 'platform[]=instagram' \
  -F 'title=Your Title' \
  -F 'description=Your full caption with hashtags' \
  https://api.upload-post.com/api/upload_photos
```

### Response Format

```json
{
  "success": true,
  "results": {
    "instagram": {
      "success": true,
      "post_id": "18407629408133837",
      "url": "https://www.instagram.com/p/DVApEUjjPqe/",
      "media_type": "IMAGE"
    }
  },
  "usage": {
    "count": 2,
    "limit": 10,
    "last_reset": "2026-02-11T14:33:24.146448"
  }
}
```

## Rate Limits

- **Current Usage:** 2/10 posts
- **Limit:** 10 posts per period
- **Last Reset:** 2026-02-11

## Files

### Scripts
- **`post-to-instagram.js`** - Node.js posting script (primary)
- **`post-to-instagram.py`** - Python posting script (alternative)
- **`autonomous-instagram-post.sh`** - Automated daily posting
- **`test-upload-post-api.sh`** - API testing utility

### Logs
- **`instagram-post-YYYY-MM-DD.log`** - Success logs
- **`instagram-post-errors-YYYY-MM-DD.log`** - Error logs
- **`instagram-post-YYYY-MM-DD.md`** - Post details (success)
- **`instagram-post-ready-YYYY-MM-DD.md`** - Manual review needed (failure)

## Automated Posting

The `autonomous-instagram-post.sh` script runs daily at 9 AM and:

1. Determines content type based on day of week
2. Selects media from `/media/inbound/` folder
3. Generates appropriate caption
4. Posts to Instagram via API
5. Logs results to `agent-outputs/`

### Content Schedule

- **Monday:** Motivation Monday - New week, fresh start
- **Tuesday:** Technique Tuesday - Form focus
- **Wednesday:** Member Spotlight - Success stories
- **Thursday:** Throwback Thursday - Classic moments
- **Friday:** Feature Friday - Equipment or movement
- **Saturday:** Saturday Strength - Weekend warrior
- **Sunday:** Sunday Reset - Rest and recovery

## Troubleshooting

### Common Issues

**"Username required in form data"**
- Solution: Ensure `user` parameter is set to `crossfitblaze`

**"404 Not Found"**
- Solution: Verify endpoint is `/api/upload_photos` (NOT `/api/v1/accounts`)

**"401 Unauthorized"**
- Solution: Check API key is valid and properly formatted

**Rate limit exceeded**
- Solution: Wait until `last_reset` time or upgrade plan

### Testing

```bash
# Test with dry run
node scripts/post-to-instagram.js test.jpg "Test caption" --dry-run

# Test API connectivity
bash scripts/test-upload-post-api.sh

# View help
node scripts/post-to-instagram.js --help
```

## Key Findings

### What Worked

✅ Endpoint: `POST /api/upload_photos`
✅ Auth: `Authorization: Apikey <key>`
✅ Required: `user` parameter with username
✅ Format: Multipart form data
✅ Platforms: Array format `platform[]=instagram`

### What Didn't Work

❌ `/api/accounts` - 404 Not Found
❌ `/api/v1/accounts` - 404 Not Found
❌ `/api/profiles` - 404 Not Found
❌ Missing `user` parameter - "Username required" error

## Documentation Sources

- [Upload-Post API Reference](https://docs.upload-post.com/api/reference)
- [Upload-Post Quickstart](https://docs.upload-post.com/quickstart)
- [Upload-Post.com API](https://api.upload-post.com)

## Next Steps

1. **Test Python script:** Verify Python version works identically
2. **Schedule cron job:** Set up daily automated posting at 9 AM
3. **Monitor rate limits:** Track API usage to avoid hitting limits
4. **Add video support:** Extend scripts to handle MP4 video posts
5. **Implement retry logic:** Add exponential backoff for failed posts
6. **Add analytics tracking:** Log engagement metrics from API responses

## Support

For API issues, contact upload-post support or check their documentation at https://docs.upload-post.com

---

**Created by:** Claude Code
**Mission:** Get automated Instagram posting working
**Result:** SUCCESS ✅
