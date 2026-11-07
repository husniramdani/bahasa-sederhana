#!/usr/bin/env node
// Hook sesi Bahasa Sederhana untuk Claude Code dan Codex.
//
// Skrip ini mencetak blok aturan dari prompts/system-prompt.md ke stdout.
// Agen membaca keluaran itu sebagai konteks tambahan di awal sesi.
// Blok aturan adalah teks di antara dua baris pertama yang isinya tepat "---".
// Jika berkas itu tidak ada atau tidak punya blok, skrip ini mencetak
// ringkasan aturan cadangan. Skrip ini selalu keluar dengan kode 0.
//
// Variabel lingkungan BAHASA_SEDERHANA_PROMPT_PATH mengganti path berkas
// prompt. Variabel ini dipakai oleh pengujian.
//
// Hanya pustaka standar Node.js.

'use strict';

const fs = require('fs');
const path = require('path');

const HEADER = 'BAHASA SEDERHANA AKTIF OTOMATIS';

const INTRO =
  'Ikuti aturan di bawah ini sejak awal sesi tanpa menunggu permintaan pengguna, ' +
  'dan baca skill lengkapnya di skills/bahasa-sederhana/SKILL.md.';

const FALLBACK = [
  'Tulis dalam bahasa Indonesia yang sederhana dan baku menurut EYD V dan KBBI.',
  'Dokumen: paling banyak 20 kata per kalimat prosedur dan 25 kata per kalimat deskripsi.',
  'Taruh syarat sebelum perintah, dan pakai "jika" untuk semua syarat.',
  'Pakai "dapat", "akan", dan "harus". Jangan pakai "sebaiknya", "mungkin", atau "seharusnya".',
  'Jangan pakai titik koma, tanda pisah, singkatan obrolan, atau kata cakapan.',
  'Balasan obrolan: jawaban di kalimat pertama, prosa saja, tanpa subjudul, butir, atau huruf tebal.',
  'Jangan ubah kode, perintah, path berkas, atau pesan kesalahan yang dikutip.',
];

function promptPath() {
  const override = process.env.BAHASA_SEDERHANA_PROMPT_PATH;
  if (override) return override;
  return path.join(__dirname, '..', '..', 'prompts', 'system-prompt.md');
}

// Kembalikan teks di antara dua baris pertama yang isinya tepat "---",
// atau null jika blok itu tidak ada atau kosong.
function extractBlock(text) {
  const lines = String(text).replace(/^﻿/, '').split(/\r?\n/);
  const marks = [];
  for (let i = 0; i < lines.length && marks.length < 2; i += 1) {
    if (lines[i] === '---') marks.push(i);
  }
  if (marks.length < 2) return null;
  const block = lines.slice(marks[0] + 1, marks[1]).join('\n').trim();
  return block.length > 0 ? block : null;
}

function buildOutput(block) {
  if (block) {
    return [HEADER, '', INTRO, '', block].join('\n') + '\n';
  }
  return [HEADER, '', ...FALLBACK].join('\n') + '\n';
}

function readBlock(file) {
  try {
    return extractBlock(fs.readFileSync(file, 'utf8'));
  } catch (err) {
    return null;
  }
}

function main() {
  let output;
  try {
    output = buildOutput(readBlock(promptPath()));
  } catch (err) {
    output = buildOutput(null);
  }
  try {
    process.stdout.write(output);
  } catch (err) {
    // Hook sesi tidak boleh menghentikan sesi.
  }
  process.exitCode = 0;
}

module.exports = { HEADER, INTRO, FALLBACK, extractBlock, buildOutput, promptPath };

if (require.main === module) {
  main();
}
