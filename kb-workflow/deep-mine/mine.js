#!/usr/bin/env node
/**
 * 统一数据挖掘入口 —— 合并10个mine-*.js为1个
 * 用法：node mine.js <mode> [options]
 * 
 * 模式：
 *   friday     → 周五采集（mine-friday.js）
 *   friday-v2  → 周五采集v2（mine-friday-v2.js）
 *   saturday   → 周六采集（mine-saturday.js）
 *   saturday-xw → 小乌周六采集（mine-saturday-xiaowu.js）
 *   tuesday    → 周二采集（mine-tuesday-v3.js，最新版）
 *   genetech   → genetech专项（mine-genetech.js）
 *   one        → 单类别挖掘（mine-one.js）
 *   robust     → 健壮版挖掘（mine-robust.js）
 *   auto       → 自动选择（根据星期几）
 */

const { execSync } = require('child_process');
const path = require('path');

const MODES = {
  'friday': 'mine-friday.js',
  'friday-v2': 'mine-friday-v2.js',
  'saturday': 'mine-saturday.js',
  'saturday-xw': 'mine-saturday-xiaowu.js',
  'tuesday': 'mine-tuesday-v3.js',
  'tuesday-v2': 'mine-tuesday-v2.js',
  'genetech': 'mine-genetech.js',
  'one': 'mine-one.js',
  'robust': 'mine-robust.js',
};

const mode = process.argv[2];
const args = process.argv.slice(3);

if (!mode || mode === '--help' || mode === '-h') {
  console.log('用法: node mine.js <mode> [options]');
  console.log('');
  console.log('可用模式:');
  Object.entries(MODES).forEach(([k, v]) => console.log(`  ${k.padEnd(15)} → ${v}`));
  console.log('  auto            → 根据星期几自动选择');
  process.exit(0);
}

let script;
if (mode === 'auto') {
  const day = new Date().getDay();
  const dayMap = { 1: 'tuesday', 2: 'tuesday', 3: 'tuesday', 4: 'tuesday', 5: 'friday-v2', 6: 'saturday-xw', 0: 'saturday-xw' };
  script = MODES[dayMap[day] || 'robust'];
  console.log(`自动选择: ${script} (星期${'日一二三四五六'[day]})`);
} else {
  script = MODES[mode];
}

if (!script) {
  console.error(`未知模式: ${mode}`);
  console.error('可用模式:', Object.keys(MODES).join(', '));
  process.exit(1);
}

const scriptPath = path.join(__dirname, script);
const cmd = `node "${scriptPath}" ${args.join(' ')}`;
console.log(`执行: ${cmd}`);

try {
  execSync(cmd, { stdio: 'inherit', cwd: process.cwd() });
} catch (e) {
  console.error(`执行失败: ${e.message}`);
  process.exit(1);
}
