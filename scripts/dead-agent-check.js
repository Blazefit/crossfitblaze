#!/usr/bin/env node
/**
 * Dead Agent Monitor
 *
 * Checks all agents in agent-manifest.json against their heartbeat files.
 * Identifies agents that haven't reported in longer than expected.
 *
 * Usage: node dead-agent-check.js [--critical-only] [--report-all]
 */

const fs = require('fs');
const path = require('path');

const MANIFEST_PATH = path.join(process.env.HOME, '.openclaw/workspace/shared-context/agent-manifest.json');
const HEARTBEAT_DIR = path.join(process.env.HOME, '.openclaw/workspace/shared-context/agent-heartbeats');
const ALERTS_DIR = path.join(process.env.HOME, '.openclaw/workspace/shared-context/alerts');

function readManifest() {
  if (!fs.existsSync(MANIFEST_PATH)) {
    throw new Error(`Manifest not found: ${MANIFEST_PATH}. Run generate-manifest.js first.`);
  }

  return JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
}

function readHeartbeat(agentName) {
  const heartbeatFile = path.join(HEARTBEAT_DIR, `${agentName}.last`);

  if (!fs.existsSync(heartbeatFile)) {
    return null;
  }

  try {
    return JSON.parse(fs.readFileSync(heartbeatFile, 'utf8'));
  } catch (error) {
    console.error(`Error reading heartbeat for ${agentName}:`, error.message);
    return null;
  }
}

function checkAgent(agent) {
  const heartbeat = readHeartbeat(agent.name);
  const now = Date.now();

  // Calculate threshold: expected interval * 1.5 (50% grace period)
  const thresholdMs = agent.expected_interval_hours * 60 * 60 * 1000 * 1.5;

  if (!heartbeat) {
    return {
      agent: agent,
      status: 'no_heartbeat',
      dead: true,
      age_hours: null,
      expected_hours: agent.expected_interval_hours,
      threshold_hours: agent.expected_interval_hours * 1.5,
      last_seen: 'never',
      reason: 'No heartbeat file found - agent never reported'
    };
  }

  const ageMs = now - heartbeat.unix_ms;
  const ageHours = ageMs / (1000 * 60 * 60);

  const isDead = ageMs > thresholdMs;

  return {
    agent: agent,
    status: isDead ? 'dead' : 'alive',
    dead: isDead,
    age_hours: ageHours,
    expected_hours: agent.expected_interval_hours,
    threshold_hours: agent.expected_interval_hours * 1.5,
    last_seen: heartbeat.timestamp,
    last_status: heartbeat.status,
    last_message: heartbeat.message || '',
    reason: isDead ? `Last seen ${ageHours.toFixed(1)}h ago (threshold: ${(agent.expected_interval_hours * 1.5).toFixed(1)}h)` : null
  };
}

function diagnoseLikelyCause(agent, result) {
  const causes = [];

  // Check cron job status from manifest
  if (agent.consecutive_errors > 0) {
    causes.push(`${agent.consecutive_errors} consecutive failures in cron job`);
  }

  if (agent.last_status === 'error') {
    causes.push('Last cron execution failed');
  }

  // Check heartbeat status
  if (result.last_status === 'error') {
    causes.push(`Last reported error: ${result.last_message || 'unknown'}`);
  }

  // Category-specific diagnoses
  if (agent.category === 'email') {
    causes.push('Possible: Gmail/Zoho auth expired, email API rate limit, network issue');
  }

  if (agent.category === 'reporting' && agent.delivery_mode === 'announce') {
    causes.push('Possible: Telegram delivery failed, message too long');
  }

  if (agent.model.includes('kimi')) {
    causes.push('Possible: Kimi K2.5 model access issue, API quota exceeded');
  }

  if (result.status === 'no_heartbeat') {
    causes.push('Agent never integrated with heartbeat system');
  }

  return causes.length > 0 ? causes : ['Unknown - requires manual investigation'];
}

function generateReport(deadAgents, allResults, options = {}) {
  const now = new Date();
  const dateStr = now.toISOString().split('T')[0];
  const timeStr = now.toISOString().split('T')[1].split(':').slice(0, 2).join('');

  // Ensure alerts directory exists
  if (!fs.existsSync(ALERTS_DIR)) {
    fs.mkdirSync(ALERTS_DIR, { recursive: true });
  }

  const reportPath = path.join(ALERTS_DIR, `dead-agents-${dateStr}-${timeStr}.md`);

  let report = `# Dead Agent Alert Report\n\n`;
  report += `**Generated:** ${now.toISOString()}\n`;
  report += `**Total Agents Monitored:** ${allResults.length}\n`;
  report += `**Dead Agents Found:** ${deadAgents.length}\n`;
  report += `**Critical Agents Dead:** ${deadAgents.filter(r => r.agent.critical).length}\n\n`;

  if (deadAgents.length === 0) {
    report += `✅ **All agents are alive and reporting normally.**\n\n`;
    report += `No action required.\n`;
  } else {
    report += `## 🚨 Dead Agents Detected\n\n`;

    // Group by criticality
    const criticalDead = deadAgents.filter(r => r.agent.critical);
    const nonCriticalDead = deadAgents.filter(r => !r.agent.critical);

    if (criticalDead.length > 0) {
      report += `### 🔥 Critical Agents (URGENT)\n\n`;

      criticalDead.forEach(result => {
        report += `#### ${result.agent.display_name}\n`;
        report += `- **Agent Name:** \`${result.agent.name}\`\n`;
        report += `- **Category:** ${result.agent.category}\n`;
        report += `- **Status:** ${result.status}\n`;
        report += `- **Last Seen:** ${result.last_seen}\n`;
        report += `- **Age:** ${result.age_hours?.toFixed(1) || 'N/A'} hours\n`;
        report += `- **Expected Interval:** ${result.expected_hours.toFixed(1)} hours\n`;
        report += `- **Threshold:** ${result.threshold_hours.toFixed(1)} hours\n`;
        report += `- **Reason:** ${result.reason}\n`;

        const causes = diagnoseLikelyCause(result.agent, result);
        report += `- **Likely Causes:**\n`;
        causes.forEach(cause => {
          report += `  - ${cause}\n`;
        });

        report += `\n`;
      });
    }

    if (nonCriticalDead.length > 0) {
      report += `### ⚠️ Non-Critical Agents\n\n`;

      nonCriticalDead.forEach(result => {
        report += `#### ${result.agent.display_name}\n`;
        report += `- **Agent Name:** \`${result.agent.name}\`\n`;
        report += `- **Category:** ${result.agent.category}\n`;
        report += `- **Last Seen:** ${result.last_seen}\n`;
        report += `- **Age:** ${result.age_hours?.toFixed(1) || 'N/A'} hours (threshold: ${result.threshold_hours.toFixed(1)}h)\n`;

        const causes = diagnoseLikelyCause(result.agent, result);
        report += `- **Likely Causes:** ${causes.join(', ')}\n`;
        report += `\n`;
      });
    }

    report += `## 📋 Action Items\n\n`;
    report += `1. **Investigate critical agents immediately** - these handle essential business functions\n`;
    report += `2. Check cron job logs: \`~/.openclaw/cron/jobs.json\` for error details\n`;
    report += `3. Verify API credentials (Gmail, Zoho, OpenRouter tokens)\n`;
    report += `4. Check system resources (disk space, memory, network)\n`;
    report += `5. Review recent config changes that might have broken agents\n\n`;
  }

  if (options.reportAll) {
    report += `## 📊 All Agent Status\n\n`;

    const aliveAgents = allResults.filter(r => r.status === 'alive');

    report += `### ✅ Alive Agents (${aliveAgents.length})\n\n`;
    report += `| Agent | Category | Last Seen | Age (hours) |\n`;
    report += `|-------|----------|-----------|-------------|\n`;

    aliveAgents
      .sort((a, b) => b.age_hours - a.age_hours)
      .forEach(result => {
        report += `| ${result.agent.name} | ${result.agent.category} | ${result.last_seen.split('T')[1].slice(0, 8)} | ${result.age_hours.toFixed(1)} |\n`;
      });
  }

  fs.writeFileSync(reportPath, report);
  return { reportPath, report, deadCount: deadAgents.length };
}

function checkAllAgents(options = {}) {
  console.log('🔍 Reading agent manifest...');
  const manifest = readManifest();

  console.log(`📊 Checking ${manifest.total_agents} agents...\n`);

  const results = [];
  let deadAgents = [];

  for (const agent of manifest.agents) {
    const result = checkAgent(agent);
    results.push(result);

    if (result.dead) {
      deadAgents.push(result);

      const icon = agent.critical ? '🔥' : '⚠️';
      console.log(`${icon} DEAD: ${agent.display_name}`);
      console.log(`   Last seen: ${result.last_seen}`);
      console.log(`   Age: ${result.age_hours?.toFixed(1) || 'N/A'} hours (threshold: ${result.threshold_hours.toFixed(1)}h)`);
      console.log(`   Reason: ${result.reason}\n`);
    }
  }

  // Filter to critical only if requested
  if (options.criticalOnly) {
    deadAgents = deadAgents.filter(r => r.agent.critical);
  }

  if (deadAgents.length === 0) {
    console.log('✅ All agents are alive and healthy!\n');
  } else {
    console.log(`\n🚨 Found ${deadAgents.length} dead agents (${deadAgents.filter(r => r.agent.critical).length} critical)\n`);
  }

  // Generate report
  const { reportPath, deadCount } = generateReport(deadAgents, results, options);
  console.log(`📄 Report written to: ${reportPath}`);

  return {
    total: results.length,
    dead: deadCount,
    critical_dead: deadAgents.filter(r => r.agent.critical).length,
    results: results,
    deadAgents: deadAgents,
    reportPath: reportPath
  };
}

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {
    criticalOnly: args.includes('--critical-only'),
    reportAll: args.includes('--report-all')
  };

  try {
    const summary = checkAllAgents(options);

    // Exit with error code if dead agents found
    process.exit(summary.dead > 0 ? 1 : 0);
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

module.exports = { checkAllAgents, checkAgent, readManifest };
