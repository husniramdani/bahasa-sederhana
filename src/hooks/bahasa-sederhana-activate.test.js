// Pengujian hook sesi. Jalankan dengan:
//   node --test src/hooks/bahasa-sederhana-activate.test.js

'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const SCRIPT = path.join(__dirname, 'bahasa-sederhana-activate.js');
const { HEADER, FALLBACK, extractBlock } = require(SCRIPT);

function run(env) {
  const result = spawnSync(process.execPath, [SCRIPT], {
    env: { ...process.env, ...env },
    encoding: 'utf8',
  });
  return result;
}

function runDefault() {
  const env = { ...process.env };
  delete env.BAHASA_SEDERHANA_PROMPT_PATH;
  return spawnSync(process.execPath, [SCRIPT], { env, encoding: 'utf8' });
}

function tempFile(content) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'bahasa-sederhana-'));
  const file = path.join(dir, 'prompt.md');
  fs.writeFileSync(file, content, 'utf8');
  return file;
}

test('keluaran diawali baris judul', () => {
  const result = runDefault();
  assert.equal(result.stdout.split('\n')[0], HEADER);
});

test('keluaran memuat blok aturan BALASAN', () => {
  const result = runDefault();
  assert.ok(result.stdout.includes('BALASAN'));
  assert.ok(result.stdout.includes('DOKUMEN'));
  assert.ok(result.stdout.includes('skills/bahasa-sederhana/SKILL.md'));
});

test('keluaran tidak memuat teks setelah garis kedua', () => {
  const result = runDefault();
  assert.ok(!result.stdout.includes('Versi hemat'));
});

test('keluaran tidak memuat teks sebelum garis pertama', () => {
  const result = runDefault();
  assert.ok(!result.stdout.includes('Prompt sistem mandiri'));
  assert.ok(!result.stdout.includes('# Blok aturan'));
  assert.ok(!result.stdout.includes('---'));
});

test('kode keluar 0 untuk berkas yang ada', () => {
  const result = runDefault();
  assert.equal(result.status, 0);
  assert.equal(result.stderr, '');
});

test('cadangan dipakai jika berkas tidak ada', () => {
  const missing = path.join(os.tmpdir(), 'tidak-ada-' + process.pid, 'system-prompt.md');
  const result = run({ BAHASA_SEDERHANA_PROMPT_PATH: missing });
  assert.equal(result.status, 0);
  const lines = result.stdout.trimEnd().split('\n');
  assert.equal(lines[0], HEADER);
  assert.equal(lines[1], '');
  const body = lines.slice(2);
  assert.ok(body.length >= 5 && body.length <= 8, 'cadangan harus 5 sampai 8 baris');
  assert.deepEqual(body, FALLBACK);
});

test('cadangan dipakai jika berkas tidak punya blok', () => {
  const file = tempFile('# Judul\n\nTidak ada garis pemisah di sini.\n');
  const result = run({ BAHASA_SEDERHANA_PROMPT_PATH: file });
  assert.equal(result.status, 0);
  assert.ok(result.stdout.startsWith(HEADER + '\n'));
  assert.ok(result.stdout.includes(FALLBACK[0]));
});

test('blok diambil dari berkas sementara', () => {
  const file = tempFile(
    'Teks pembuka yang tidak boleh muncul.\n---\nATURAN SATU\n\nATURAN DUA\n---\nTeks penutup yang tidak boleh muncul.\n---\nBlok ketiga.\n'
  );
  const result = run({ BAHASA_SEDERHANA_PROMPT_PATH: file });
  assert.equal(result.status, 0);
  assert.ok(result.stdout.includes('ATURAN SATU\n\nATURAN DUA'));
  assert.ok(!result.stdout.includes('pembuka'));
  assert.ok(!result.stdout.includes('penutup'));
  assert.ok(!result.stdout.includes('Blok ketiga'));
  const lines = result.stdout.split('\n');
  assert.equal(lines[0], HEADER);
  assert.equal(lines[1], '');
  assert.ok(lines[2].includes('skills/bahasa-sederhana/SKILL.md'));
  assert.equal(lines[3], '');
  assert.equal(lines[4], 'ATURAN SATU');
});

test('extractBlock hanya menerima baris yang tepat ---', () => {
  assert.equal(extractBlock('a\n --- \nb\n----\nc'), null);
  assert.equal(extractBlock('a\r\n---\r\nisi\r\n---\r\nb'), 'isi');
  assert.equal(extractBlock('---\n\n---\n'), null);
});
