#!/usr/bin/env bash
#
# Test script for upload-post API endpoint discovery
# Tests the upload_photos endpoint with CrossFit Blaze account

set -e

API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImNvc2RhbmVlbG9saXZhd0BnbWFpbC5jb20iLCJleHAiOjQ5MjQ0MjA2MTIsImp0aSI6IjM0YThjZmU1LWY1NDEtNGUwZC1hZDI0LTNlNGMwMWI5YzRiOSJ9.DC0JGSRvMMnk5oBLPaNNS9-FzMIP2kKdOWuRBmjciKU"
API_BASE="https://api.upload-post.com/api"
TEST_IMAGE="/Users/daneel/.openclaw/workspace/media/inbound/file_34---285e545e-7620-412c-be03-41b7faf09ffd.jpg"

echo "=== Upload-Post API Test ==="
echo "API Base: $API_BASE"
echo "Test Image: $TEST_IMAGE"
echo ""

# Check if test image exists
if [ ! -f "$TEST_IMAGE" ]; then
    echo "❌ Test image not found: $TEST_IMAGE"
    exit 1
fi

echo "✅ Test image exists"
echo ""

# Test 1: Check if we need a user parameter
echo "Test 1: Checking user management requirements..."
curl -s -X GET \
    -H "Authorization: Apikey $API_KEY" \
    "$API_BASE/user" | jq '.' || echo "User endpoint check failed"
echo ""

# Test 2: Try basic photo upload
echo "Test 2: Testing photo upload endpoint (DRY RUN - no actual post)..."
echo "Endpoint: POST $API_BASE/upload_photos"
echo ""

# Show what would be sent
echo "Request parameters:"
echo "  - photos[]: $TEST_IMAGE"
echo "  - platform[]: instagram"
echo "  - title: Test API Connection"
echo "  - description: Testing upload-post API integration for CrossFit Blaze automation"
echo ""

echo "To perform actual upload, run the post-to-instagram.js script"
echo ""

# Test 3: Check API key validity
echo "Test 3: Validating API key..."
response=$(curl -s -w "\n%{http_code}" -X POST \
    -H "Authorization: Apikey $API_KEY" \
    -F "test=true" \
    "$API_BASE/upload_photos")

http_code=$(echo "$response" | tail -1)
body=$(echo "$response" | head -n -1)

echo "HTTP Status: $http_code"
echo "Response: $body"
echo ""

if [ "$http_code" = "200" ] || [ "$http_code" = "400" ]; then
    echo "✅ API key is valid (endpoint responded)"
elif [ "$http_code" = "401" ] || [ "$http_code" = "403" ]; then
    echo "❌ API key authentication failed"
    exit 1
elif [ "$http_code" = "404" ]; then
    echo "⚠️  Endpoint not found - may need different path"
else
    echo "⚠️  Unexpected response code: $http_code"
fi

echo ""
echo "=== Test Complete ==="
echo "Next step: Use post-to-instagram.js to perform actual uploads"
