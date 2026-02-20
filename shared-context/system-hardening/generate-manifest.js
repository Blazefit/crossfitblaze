#!/usr/bin/env node
/**
 * Agent Manifest Generator
 *
 * Parses ~/.openclaw/cron/jobs.json and generates agent-manifest.json
 * This manifest tracks all cron jobs (agents) with their expected intervals
 * for dead agent detection.
 */

const fs = require('fs');
const path = require('path');

// Parse cron expression to get expected interval in hours
function cronToHours(cronExpr) {
  const parts = cronExpr.split(' ');

  // Handle simple patterns
  if (cronExpr.includes('* * *')) {
    // Hourly patterns like "0 * * * *" = every hour
    return 1;
  }

  if (cronExpr.includes(',')) {
    // Multiple times per day like "0 8,10,12,14,16,18,20,22 * * *"
    const hours = parts[1].split(',');
    return 24 / hours.length;
  }

  if (parts[1] === '*' && parts[2] === '*' && parts[3] === '*' && parts[4] === '*') {
    // Every X minutes like "*/30 * * * *"
    if (parts[0].includes('*/')) {
      const minutes = parseInt(parts[0].split('/')[1]);
      return minutes / 60;
    }
    return 1;
  }

  // Check for weekly patterns
  if (parts[4] && parts[4] !== '*') {
    // Day of week specified = weekly
    return 168; // 7 days * 24 hours
  }

  // Default: once per day
  return 24;
}

// Parse "every" schedule to hours
function everyMsToHours(everyMs) {
  return everyMs / (1000 * 60 * 60);
}

// Extract output path pattern from job message
function extractOutputPath(message) {
  if (!message) return null;

  // Look for output path patterns in the message
  const match = message.match(/shared-context\/agent-outputs\/([^\s]+)/);
  if (match) {
    return `shared-context/agent-outputs/${match[1]}`;
  }

  // Default pattern
  return 'shared-context/agent-outputs/';
}

// Determine agent name from job name
function extractAgentName(jobName) {
  // Convert "Daily Briefing 5am" -> "briefing-daily"
  // Convert "Night Owl - Overnight Specialist" -> "nightowl-overnight"
  // Convert "Closer - Lead Manager Morning" -> "closer-morning"

  const cleaned = jobName
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');

  return cleaned;
}

// Categorize job type
function categorizeJob(jobName, message) {
  const name = jobName.toLowerCase();
  const msg = (message || '').toLowerCase();

  if (name.includes('switch to') || name.includes('model')) return 'system';
  if (name.includes('health') || name.includes('check') || name.includes('debugger')) return 'monitoring';
  if (name.includes('briefing') || name.includes('summary') || name.includes('report')) return 'reporting';
  if (name.includes('email') || name.includes('inbox')) return 'email';
  if (name.includes('content') || name.includes('spark')) return 'content';
  if (name.includes('lead') || name.includes('closer')) return 'sales';
  if (name.includes('outreach')) return 'engagement';
  if (name.includes('strategist') || name.includes('planning')) return 'strategy';
  if (name.includes('builder')) return 'automation';
  if (name.includes('ops')) return 'operations';
  if (name.includes('freelance') || name.includes('bounty')) return 'revenue';
  if (name.includes('night owl') || name.includes('overnight')) return 'overnight';

  return 'general';
}

function generateManifest() {
  const cronJobsPath = path.join(process.env.HOME, '.openclaw/cron/jobs.json');
  const outputPath = path.join(process.env.HOME, '.openclaw/workspace/shared-context/agent-manifest.json');

  console.log('Reading cron jobs from:', cronJobsPath);

  const cronData = JSON.parse(fs.readFileSync(cronJobsPath, 'utf8'));
  const agents = [];

  for (const job of cronData.jobs) {
    // Skip disabled jobs
    if (!job.enabled) {
      console.log(`Skipping disabled job: ${job.name}`);
      continue;
    }

    let expectedIntervalHours;
    let scheduleType;
    let scheduleExpr;

    if (job.schedule.kind === 'cron') {
      scheduleType = 'cron';
      scheduleExpr = job.schedule.expr;
      expectedIntervalHours = cronToHours(job.schedule.expr);
    } else if (job.schedule.kind === 'every') {
      scheduleType = 'interval';
      scheduleExpr = `every ${job.schedule.everyMs}ms`;
      expectedIntervalHours = everyMsToHours(job.schedule.everyMs);
    } else if (job.schedule.kind === 'at') {
      // One-time scheduled jobs - skip these
      console.log(`Skipping one-time job: ${job.name}`);
      continue;
    } else {
      scheduleType = 'unknown';
      scheduleExpr = JSON.stringify(job.schedule);
      expectedIntervalHours = 24; // Default
    }

    const agentName = extractAgentName(job.name);
    const message = job.payload?.message || '';
    const outputPath = extractOutputPath(message);
    const model = job.payload?.model || 'unknown';
    const category = categorizeJob(job.name, message);

    // Determine criticality
    const isCritical =
      category === 'email' ||
      category === 'reporting' ||
      category === 'sales' ||
      job.name.includes('Briefing') ||
      job.name.includes('Inbox');

    agents.push({
      id: job.id,
      name: agentName,
      display_name: job.name,
      category: category,
      critical: isCritical,
      schedule_type: scheduleType,
      schedule: scheduleExpr,
      expected_interval_hours: expectedIntervalHours,
      output_path: outputPath,
      model: model,
      last_status: job.state?.lastStatus || 'unknown',
      consecutive_errors: job.state?.consecutiveErrors || 0,
      delivery_mode: job.delivery?.mode || 'none'
    });
  }

  const manifest = {
    generated_at: new Date().toISOString(),
    total_agents: agents.length,
    critical_agents: agents.filter(a => a.critical).length,
    agents: agents.sort((a, b) => {
      // Sort: critical first, then by category, then by name
      if (a.critical !== b.critical) return b.critical - a.critical;
      if (a.category !== b.category) return a.category.localeCompare(b.category);
      return a.name.localeCompare(b.name);
    })
  };

  fs.writeFileSync(outputPath, JSON.stringify(manifest, null, 2));
  console.log(`\n✅ Manifest generated: ${outputPath}`);
  console.log(`📊 Total agents: ${manifest.total_agents}`);
  console.log(`🔥 Critical agents: ${manifest.critical_agents}`);

  // Print summary by category
  const byCategory = {};
  agents.forEach(a => {
    byCategory[a.category] = (byCategory[a.category] || 0) + 1;
  });

  console.log('\n📋 Agents by category:');
  Object.entries(byCategory)
    .sort(([, a], [, b]) => b - a)
    .forEach(([cat, count]) => {
      console.log(`   ${cat}: ${count}`);
    });

  return manifest;
}

// Run if called directly
if (require.main === module) {
  try {
    generateManifest();
  } catch (error) {
    console.error('❌ Error generating manifest:', error.message);
    process.exit(1);
  }
}

module.exports = { generateManifest };
