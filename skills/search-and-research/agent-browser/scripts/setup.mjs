#!/usr/bin/env node
/**
 * Setup verification for agent-browser skill.
 * Run with: node scripts/setup.mjs
 */

import { execSync, spawnSync } from 'child_process';

function checkAgentBrowserInstalled() {
  try {
    execSync('which agent-browser', { stdio: 'pipe' });
    return true;
  } catch {
    console.error('ERROR: agent-browser not found in PATH');
    console.error('\nInstall with: npm install -g agent-browser');
    return false;
  }
}

function getVersion() {
  try {
    const result = spawnSync('agent-browser', ['--version'], { encoding: 'utf-8' });
    if (result.status === 0) {
      console.log(`agent-browser version: ${result.stdout.trim()}`);
      return true;
    }
  } catch {
    // Fall through
  }
  console.error('ERROR: agent-browser not responding');
  return false;
}

function checkBrowserInstalled() {
  try {
    const result = spawnSync('agent-browser', ['install', '--check'], { encoding: 'utf-8' });
    if (result.status === 0) {
      return true;
    }
  } catch {
    // Fall through
  }
  console.error('ERROR: Chromium not installed');
  console.error('\nInstall with: agent-browser install');
  return false;
}

function main() {
  console.log('Checking agent-browser installation...\n');

  if (!checkAgentBrowserInstalled()) {
    process.exit(1);
  }

  if (!getVersion()) {
    process.exit(1);
  }

  if (!checkBrowserInstalled()) {
    process.exit(1);
  }

  console.log('\n✓ agent-browser is installed and ready');
  process.exit(0);
}

main();
