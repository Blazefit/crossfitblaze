#!/usr/bin/env node
const https = require('https');

// Fetch jobs
const options = {
  hostname: 'www.openwork.bot',
  path: '/api/jobs/match',
  method: 'GET',
  headers: {
    'Authorization': 'Bearer ow_8b63e597f555df54165815de4be9d6fa88a9932f4740d06d'
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    try {
      const jobs = JSON.parse(data);
      
      // Filter for paying jobs
      const payingJobs = jobs.filter(j => 
        j.reward > 0 && 
        !j.title.includes('Welcome') && 
        !j.title.includes('introduce yourself')
      );
      
      console.log('=== PAYING JOBS FOUND ===\n');
      payingJobs.forEach(j => {
        console.log(`${j.id}`);
        console.log(`Title: ${j.title}`);
        console.log(`Reward: ${j.reward.toLocaleString()} $OPENWORK`);
        console.log(`Status: ${j.status}`);
        console.log('---');
      });
      console.log(`\nTotal paying jobs: ${payingJobs.length}`);
    } catch (e) {
      console.error('Error parsing:', e.message);
    }
  });
});

req.on('error', (e) => console.error('Request error:', e));
req.end();
