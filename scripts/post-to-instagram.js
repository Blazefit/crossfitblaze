#!/usr/bin/env node
/**
 * Instagram Post Automation via upload-post API
 * Posts images with captions to @crossfitblaze Instagram account
 *
 * Usage: node post-to-instagram.js <image_path> <caption> [--dry-run]
 * Example: node post-to-instagram.js ./image.jpg "Great workout! #CrossFit"
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Configuration
const API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImNvc2RhbmVlbG9saXZhd0BnbWFpbC5jb20iLCJleHAiOjQ5MjQ0MjA2MTIsImp0aSI6IjM0YThjZmU1LWY1NDEtNGUwZC1hZDI0LTNlNGMwMWI5YzRiOSJ9.DC0JGSRvMMnk5oBLPaNNS9-FzMIP2kKdOWuRBmjciKU';
const API_BASE = 'https://api.upload-post.com';
const UPLOAD_ENDPOINT = '/api/upload_photos';

/**
 * Create multipart form data boundary and body
 */
function createMultipartBody(imagePath, caption, dryRun = false) {
    const boundary = '----WebKitFormBoundary' + Math.random().toString(36).substring(2);
    const imageBuffer = fs.readFileSync(imagePath);
    const imageFilename = path.basename(imagePath);
    const mimeType = imagePath.toLowerCase().endsWith('.png') ? 'image/png' : 'image/jpeg';

    let body = '';

    // Add photo file
    body += `--${boundary}\r\n`;
    body += `Content-Disposition: form-data; name="photos[]"; filename="${imageFilename}"\r\n`;
    body += `Content-Type: ${mimeType}\r\n\r\n`;

    const bodyParts = [
        Buffer.from(body, 'utf8'),
        imageBuffer,
        Buffer.from('\r\n', 'utf8')
    ];

    // Add user/username (required by API)
    body = `--${boundary}\r\n`;
    body += `Content-Disposition: form-data; name="user"\r\n\r\n`;
    body += `crossfitblaze\r\n`;
    bodyParts.push(Buffer.from(body, 'utf8'));

    // Add platform
    body = `--${boundary}\r\n`;
    body += `Content-Disposition: form-data; name="platform[]"\r\n\r\n`;
    body += `instagram\r\n`;
    bodyParts.push(Buffer.from(body, 'utf8'));

    // Add description (caption)
    body = `--${boundary}\r\n`;
    body += `Content-Disposition: form-data; name="description"\r\n\r\n`;
    body += `${caption}\r\n`;
    bodyParts.push(Buffer.from(body, 'utf8'));

    // Add title (first line of caption)
    const title = caption.split('\n')[0].substring(0, 100);
    body = `--${boundary}\r\n`;
    body += `Content-Disposition: form-data; name="title"\r\n\r\n`;
    body += `${title}\r\n`;
    bodyParts.push(Buffer.from(body, 'utf8'));

    // Close boundary
    body = `--${boundary}--\r\n`;
    bodyParts.push(Buffer.from(body, 'utf8'));

    return {
        boundary,
        body: Buffer.concat(bodyParts)
    };
}

/**
 * Post to Instagram via upload-post API
 */
function postToInstagram(imagePath, caption, dryRun = false) {
    return new Promise((resolve, reject) => {
        // Validate inputs
        if (!fs.existsSync(imagePath)) {
            return reject(new Error(`Image file not found: ${imagePath}`));
        }

        if (!caption || caption.trim().length === 0) {
            return reject(new Error('Caption is required'));
        }

        if (dryRun) {
            console.log('🔍 DRY RUN MODE - No actual post will be made');
            console.log('Image:', imagePath);
            console.log('Caption:', caption);
            console.log('Platform: Instagram (@crossfitblaze)');
            return resolve({
                success: true,
                dryRun: true,
                message: 'Dry run completed successfully'
            });
        }

        // Create multipart form data
        const { boundary, body } = createMultipartBody(imagePath, caption, dryRun);

        // Prepare request options
        const options = {
            hostname: 'api.upload-post.com',
            port: 443,
            path: UPLOAD_ENDPOINT,
            method: 'POST',
            headers: {
                'Authorization': `Apikey ${API_KEY}`,
                'Content-Type': `multipart/form-data; boundary=${boundary}`,
                'Content-Length': body.length
            }
        };

        console.log('📤 Uploading to Instagram...');
        console.log('Image:', path.basename(imagePath));
        console.log('Caption length:', caption.length, 'characters');

        // Make request
        const req = https.request(options, (res) => {
            let responseData = '';

            res.on('data', (chunk) => {
                responseData += chunk;
            });

            res.on('end', () => {
                console.log('Response status:', res.statusCode);

                let parsedResponse;
                try {
                    parsedResponse = JSON.parse(responseData);
                } catch (e) {
                    parsedResponse = { raw: responseData };
                }

                if (res.statusCode >= 200 && res.statusCode < 300) {
                    console.log('✅ Post successful!');
                    resolve({
                        success: true,
                        statusCode: res.statusCode,
                        data: parsedResponse
                    });
                } else {
                    console.error('❌ Post failed');
                    console.error('Response:', responseData);
                    reject(new Error(`API request failed with status ${res.statusCode}: ${responseData}`));
                }
            });
        });

        req.on('error', (error) => {
            console.error('❌ Request error:', error.message);
            reject(error);
        });

        // Send request body
        req.write(body);
        req.end();
    });
}

/**
 * Main execution
 */
async function main() {
    const args = process.argv.slice(2);

    if (args.length < 2 || args.includes('--help') || args.includes('-h')) {
        console.log('Usage: node post-to-instagram.js <image_path> <caption> [--dry-run]');
        console.log('');
        console.log('Arguments:');
        console.log('  image_path    Path to image file (jpg, jpeg, png)');
        console.log('  caption       Instagram post caption');
        console.log('  --dry-run     Test without actually posting');
        console.log('');
        console.log('Example:');
        console.log('  node post-to-instagram.js ./workout.jpg "Great session! 💪 #CrossFit"');
        process.exit(args.includes('--help') || args.includes('-h') ? 0 : 1);
    }

    const imagePath = path.resolve(args[0]);
    const caption = args[1];
    const dryRun = args.includes('--dry-run');

    console.log('=== CrossFit Blaze Instagram Post ===');
    console.log('Account: @crossfitblaze');
    console.log('');

    try {
        const result = await postToInstagram(imagePath, caption, dryRun);

        if (result.success) {
            console.log('');
            console.log('📊 Result:');
            console.log(JSON.stringify(result, null, 2));

            if (!dryRun && result.data) {
                // Log success to file
                const logDir = '/Users/daneel/.openclaw/workspace/shared-context/agent-outputs';
                const logFile = path.join(logDir, `instagram-post-${new Date().toISOString().split('T')[0]}.log`);
                const logEntry = `[${new Date().toISOString()}] SUCCESS: ${path.basename(imagePath)}\n${caption}\n---\n`;
                fs.appendFileSync(logFile, logEntry);
            }

            process.exit(0);
        }
    } catch (error) {
        console.error('');
        console.error('💥 Error:', error.message);

        // Log error to file
        const logDir = '/Users/daneel/.openclaw/workspace/shared-context/agent-outputs';
        const errorFile = path.join(logDir, `instagram-post-errors-${new Date().toISOString().split('T')[0]}.log`);
        const errorEntry = `[${new Date().toISOString()}] ERROR: ${error.message}\nImage: ${imagePath}\n---\n`;
        fs.appendFileSync(errorFile, errorEntry);

        process.exit(1);
    }
}

// Run if called directly
if (require.main === module) {
    main();
}

module.exports = { postToInstagram };
