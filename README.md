# Bahasa Sederhana

Skill untuk agen AI yang menulis bahasa Indonesia sederhana dan baku. Pembaca memahami teksnya dalam sekali baca, tanpa jargon dan tanpa gaya tulisan AI.

<p>
  <a href="skills/bahasa-sederhana/SKILL.md"><img src="https://img.shields.io/badge/versi-1.0.0-blue?style=flat" alt="versi 1.0.0"></a>
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/SKILL.md-standar_terbuka-blue?style=flat" alt="Agent Skills"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/lisensi-MIT-lightgrey?style=flat" alt="MIT"></a>
</p>

Aturannya memakai disiplin [ASD-STE100](https://www.asd-ste100.org/), standar bahasa terkendali untuk manual teknis. Setiap aturan disesuaikan dengan tata bahasa Indonesia, EYD Edisi V, dan KBBI. Aturan yang tidak cocok untuk bahasa Indonesia diganti. Aturan khusus bahasa Indonesia ditambahkan.

Skill ini dapat dipakai di setiap agen yang membaca [standar Agent Skills](https://agentskills.io). Contohnya Claude Code, Cursor, VS Code Copilot, OpenAI Codex, Gemini CLI, dan OpenCode.

## Contoh

Teks pertama adalah gaya tulisan AI berbahasa Indonesia yang umum. Teks kedua adalah isi yang sama setelah skill ini dipakai.

Tanpa skill:

> kirimlog adalah merupakan sebuah tool CLI yang dirancang untuk mengirimkan log-log aplikasi Anda ke OpenSearch, yang mana memungkinkan tim Anda untuk memonitor sistem secara mulus. Sebelum memulai, Anda sebaiknya memastikan index tujuan telah dibuat — hal ini sangat krusial untuk menghindari error di kemudian hari.

Dengan skill:

> Alat baris perintah kirimlog mengirim log aplikasi ke OpenSearch.
>
> Buat indeks tujuan sebelum Anda menjalankan kirimlog. Jika indeks itu belum ada, kirimlog tidak dapat mengirim data.

Contoh lain ada di [`examples/sebelum-sesudah.md`](examples/sebelum-sesudah.md). Contoh itu mencakup README, pemecahan masalah, pesan kesalahan, laporan insiden, catatan rilis, terjemahan, dan balasan obrolan.

## Pemasangan

Pilih satu cara.

Untuk semua agen, dengan [skills CLI](https://github.com/vercel-labs/skills). Cara ini hanya memasang skill:

```bash
npx skills add husniramdani/bahasa-sederhana
```

Untuk Claude Code, dengan hook dan gaya keluaran:

```bash
claude plugin marketplace add husniramdani/bahasa-sederhana
claude plugin install bahasa-sederhana@bahasa-sederhana
```

Untuk memakai gaya keluaran, buka `/config` dan pilih `bahasa-sederhana:bahasa-sederhana` di bagian *Output style*.

Untuk Codex, dengan hook sesi:

```bash
codex plugin marketplace add husniramdani/bahasa-sederhana
codex plugin add bahasa-sederhana@bahasa-sederhana
```

Hook membutuhkan Node.js dan Python 3. Penjelasan setiap hook ada di [`src/hooks/README.md`](src/hooks/README.md).

Jika alat Anda tidak membaca skill, salin blok aturan dari [`prompts/system-prompt.md`](prompts/system-prompt.md) ke prompt sistem, `AGENTS.md`, atau `.cursorrules`.

## Cara memakai

Ketik `/bahasa-sederhana`, lalu tempel teks Anda atau jelaskan dokumen yang Anda butuhkan. Permintaan biasa juga berhasil, misalnya "tulis ulang README ini dengan bahasa sederhana".

Teks sumber boleh berbahasa Inggris. Hasilnya selalu bahasa Indonesia. Skill ini menerjemahkan makna, bukan susunan kata.

## Isi aturan

[`SKILL.md`](skills/bahasa-sederhana/SKILL.md) punya dua ragam. Ragam Dokumen berlaku untuk teks yang Anda simpan: dokumentasi, README, runbook, pesan kesalahan, dan catatan rilis. Ragam Balasan berlaku untuk jawaban di obrolan.

Ragam Dokumen:

| Aturan | Contoh yang dihindari |
|---|---|
| Paling banyak 20 kata per kalimat instruksi, 25 per kalimat deskripsi | Kalimat panjang dengan tiga anak kalimat |
| Syarat sebelum perintah, selalu dengan "jika" | "Baca log apabila tes gagal." |
| Kalimat perintah langsung | "Silakan melakukan penghapusan berkas." |
| Modalitas dapat, akan, harus | "sebaiknya", "mungkin", "seharusnya" |
| Satu kata untuk satu makna | "cek", "periksa", dan "verifikasi" dalam satu dokumen |
| Ejaan EYD V dan bentuk baku KBBI | "merubah", "dimana", "anda", "resiko" |
| Tanpa struktur kalimat bahasa Inggris | "server di mana aplikasi berjalan", "melakukan pengecekan" |
| Istilah teknis yang dikenal pembaca | Padanan resmi yang jarang dipakai, atau istilah Inggris yang sudah punya padanan umum |
| Fakta, bukan hiasan | "krusial", "tangguh", "tidak hanya X, tetapi juga Y" |

Ragam Balasan:

| Aturan | Contoh yang dihindari |
|---|---|
| Prosa saja | Subjudul, butir, dan huruf tebal untuk jawaban pendek |
| Jawaban di kalimat pertama | "Pertanyaan yang bagus!" |
| Tanpa tanda pisah | Dua pikiran yang disambung tanpa kata hubung |
| Istilah dijelaskan singkat | Jargon tanpa penjelasan |
| Tanpa pembuka dan penutup basa-basi | "Tentu!" dan "Semoga membantu!" |

Katalog lengkap dengan kode BS1.1 sampai BS10.10 ada di [`katalog-aturan.md`](skills/bahasa-sederhana/references/katalog-aturan.md).

## Dua mode

Mode Sederhana adalah bawaannya. Mode ini memakai istilah yang dikenal pembaca, misalnya *server*.

Mode Baku berlaku jika Anda menyebut EYD, KBBI, bahasa baku, dokumen resmi, atau Perpres 63/2019. Mode ini memakai padanan resmi, misalnya "peladen (*server*)", dan aturan ejaan yang lebih ketat dari [`mode-baku.md`](skills/bahasa-sederhana/references/mode-baku.md).

Balasan obrolan selalu memakai Mode Sederhana.

## Penyesuaian untuk bahasa Indonesia

ASD-STE100 ditulis untuk bahasa Inggris. Tabel ini menunjukkan aturan yang diganti. Catatan risetnya ada di [`docs/riset.md`](docs/riset.md).

| Aturan STE untuk bahasa Inggris | Bahasa Sederhana | Alasan |
|---|---|---|
| Kala sederhana | Keterangan waktu yang jelas | Bahasa Indonesia tidak punya kala. |
| Hindari kalimat pasif | Kalimat perintah untuk langkah, pasif di- boleh dalam deskripsi | Pasif di- adalah bentuk yang wajar dalam bahasa Indonesia. |
| Pertahankan artikel | Pertahankan kata tugas: "bahwa", "yang", "untuk", subjek | Bahasa Indonesia tidak punya artikel. |
| Tanpa kontraksi | Tanpa singkatan obrolan dan kata cakapan | Padanannya adalah "yg", "gak", "udah". |
| Kamus kata yang disetujui | Mode Baku dengan EYD V, KBBI, dan Pasti | Bahasa Indonesia tidak punya kamus bahasa terkendali. |
| Tidak ada | Format angka: 12,5%, Rp15.000, pukul 09.30 | EYD V memakai koma desimal dan titik ribuan. |
| Tidak ada | "di mana" bukan kata penghubung, tanpa "melakukan" ditambah kata benda | Kesalahan terjemahan dari bahasa Inggris yang paling sering muncul. |
| Tidak ada | Kebijakan istilah teknis tiga kelompok | Sebagian padanan resmi belum dikenal luas. |
| Tidak ada | "Anda" selalu kapital, satu sapaan per dokumen | Kesalahan sapaan sering muncul di teks produk. |

## Linter

[`evals/bahasa_lint.py`](evals/bahasa_lint.py) menghitung pelanggaran yang dapat ditemukan dengan pola teks. Linter ini memakai Python 3 tanpa pustaka tambahan.

```bash
python3 evals/bahasa_lint.py --type procedural panduan.md
python3 evals/bahasa_lint.py --type descriptive catatan-rilis.md
python3 evals/bahasa_lint.py --self-test
```

Linter ini memeriksa 14 jenis pelanggaran, termasuk kata tidak baku, kata gaya AI, terjemahan harfiah, dan sinonim yang berganti-ganti. Daftar katanya ada di `evals/nonbaku.tsv` dan `evals/slop.tsv`.

Linter ini membaca pola, bukan makna. Pakai linter ini untuk membandingkan dua versi teks, bukan sebagai bukti bahwa teks sudah benar.

## Benchmark

Belum ada hasil benchmark. Skenarionya ada di `evals/scenarios.json` dan `evals/reply_scenarios.json`. Untuk menjalankannya, Anda butuh Claude Code CLI yang sudah masuk:

```bash
python3 evals/run_bench.py --smoke
python3 evals/run_reply_bench.py --skill bahasa-sederhana=prompts/system-prompt.md --out evals/results/balasan
```

Skenario uji manual ada di [`evals/pressure-tests.md`](evals/pressure-tests.md).

## Tanya jawab

Apakah hasilnya pasti sesuai EYD dan KBBI? Tidak. Tidak ada alat yang menjaminnya. Mode Baku membuat hasilnya lebih dekat. Acuan resminya dapat dibaca gratis di ejaan.kemdikbud.go.id dan kbbi.kemdikbud.go.id.

Apakah dokumennya akan terasa kaku? Dokumennya akan terasa datar, seperti manual teknis. Untuk dokumentasi, sifat itu membuat teks sulit disalahpahami. Untuk blog dan pemasaran, pakai gaya Anda sendiri.

Mengapa *server* tidak diganti "peladen"? Dalam Mode Sederhana, pembaca harus mengenali istilahnya. Mode Baku memakai "peladen" dan menulis *server* dalam kurung.

## Kontribusi

Laporkan kesalahan atau usulan di *issue*. Sebelum Anda mengirim *pull request*, jalankan tiga pemeriksaan ini:

```bash
python3 evals/bahasa_lint.py --self-test
node --test src/hooks/bahasa-sederhana-activate.test.js
python3 src/hooks/test_lint_hook.py
```

Jika Anda menambah kata ke `evals/nonbaku.tsv` atau `evals/slop.tsv`, sebut sumbernya di *pull request*.

## Lisensi

MIT. Repositori ini merangkum aturan dengan kata-kata sendiri dan tidak menyalin teks ASD-STE100, EYD V, atau KBBI. Proyek ini tidak resmi dan tidak berafiliasi dengan ASD atau Badan Pengembangan dan Pembinaan Bahasa. ASD-STE100 adalah merek dagang terdaftar milik ASD.
