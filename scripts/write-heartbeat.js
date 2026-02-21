#!/usr/bin/env node
/**
 * Heartbeat Writer
 *
 * Allows agents to write heartbeat timestamps on successful completion.
 * Usage: node write-heartbeat.js <agent-name> [status] [message]
 *
 * Example:
 *   node write-heartbeat.js briefing-daily ok "Daily briefing sent"
 *   node write-heartbeat.js closer-morning error "Gmail auth failed"
 */

const fs = require('fs');
const path = require('path');

const HEARTBEAT_DIR = path.join(process.env.HOME, '.openclaw/workspace/shared-context/agent-heartbeats');

function writeHeartbeat(agentName, status = 'ok', message = '') {
  // Ensure directory exists
  if (!fs.existsSync(HEARTBEAT_DIR)) {
    fs.mkdirSync(HEARTBEAT_DIR, { recursive: true });
  }

  const heartbeatFile = path.join(HEARTBEAT_DIR, `${agentName}.last`);
  const timestamp = new Date().toISOString();

  const heartbeatData = {
    agent: agentName,
    timestamp: timestamp,
    status: status,
    message: message || '',
    unix_ms: Date.now()
  };

  fs.writeFileSync(heartbeatFile, JSON.stringify(heartbeatData, null, 2));

  if (process.env.VERBOSE) {
    console.log(`✅ Heartbeat written for ${agentName}: ${status}`);
  }

  return heartbeatData;
}

function readHeartbeat(agentName) {
  const heartbeatFile = path.join(HEARTBEAT_DIR, `${agentName}.last`);

  if (!fs.existsSync(heartbeatFile)) {
    return null;
  }

  try {
    const data = fs.readFileSync(heartbeatFile, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error(`Error reading heartbeat for ${agentName}:`, error.message);
    return null;
  }
}

function listHeartbeats() {
  if (!fs.existsSync(HEARTBEAT_DIR)) {
    return [];
  }

  const files = fs.readdirSync(HEARTBEAT_DIR).filter(f => f.endsWith('.last'));
  const heartbeats = [];

  for (const file of files) {
    const agentName = file.replace('.last', '');
    const data = readHeartbeat(agentName);
    if (data) {
      heartbeats.push(data);
    }
  }

  return heartbeats.sort((a, b) => b.unix_ms - a.unix_ms);
}

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Usage: node write-heartbeat.js <agent-name> [status] [message]');
    console.log('       node write-heartbeat.js --list');
    console.log('       node write-heartbeat.js --read <agent-name>');
    process.exit(1);
  }

  if (args[0] === '--list') {
    const heartbeats = listHeartbeats();
    console.log(`📊 Total heartbeats: ${heartbeats.length}\n`);

    heartbeats.forEach(hb => {
      const age = Math.floor((Date.now() - hb.unix_ms) / 1000 / 60);
      console.log(`${hb.agent.padEnd(35)} | ${hb.status.padEnd(8)} | ${age}m ago | ${hb.message || '(no message)'}`);
    });

    process.exit(0);
  }

  if (args[0] === '--read') {
    const agentName = args[1];
    if (!agentName) {
      console.error('Error: Agent name required');
      process.exit(1);
    }

    const data = readHeartbeat(agentName);
    if (!data) {
      console.error(`No heartbeat found for ${agentName}`);
      process.exit(1);
    }

    console.log(JSON.stringify(data, null, 2));
    process.exit(0);
  }

  const [agentName, status = 'ok', ...messageParts] = args;
  const message = messageParts.join(' ');

  try {
    writeHeartbeat(agentName, status, message);
    console.log(`✅ Heartbeat written for ${agentName}`);
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

module.exports = { writeHeartbeat, readHeartbeat, listHeartbeats };
