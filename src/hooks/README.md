# Hook Bahasa Sederhana

Folder ini berisi tiga *hook* untuk plugin Bahasa Sederhana. *Hook* adalah perintah yang dijalankan agen pada peristiwa tertentu, misalnya saat sesi dimulai. Claude Code memakai ketiga hook itu. Codex hanya memakai hook sesi.

| Hook | Berkas | Peristiwa |
|---|---|---|
| Hook sesi | `bahasa-sederhana-activate.js` | `SessionStart` |
| Hook pemeriksaan berkas | `lint_hook.py` | `PostToolUse` untuk `Write` dan `Edit` |
| Hook pemeriksaan balasan | `lint_hook.py` | `Stop` |

## Kebutuhan

Hook sesi membutuhkan Node.js versi 18 atau yang lebih baru. Hook pemeriksaan berkas dan hook pemeriksaan balasan membutuhkan Python 3. Ketiga hook hanya memakai pustaka standar, jadi Anda tidak perlu memasang paket tambahan.

## Pemasangan

Untuk Claude Code, pasang plugin dengan dua perintah ini:

```bash
claude plugin marketplace add husniramdani/bahasa-sederhana
claude plugin install bahasa-sederhana@bahasa-sederhana
```

Untuk Codex, pasang plugin dengan dua perintah ini:

```bash
codex plugin marketplace add husniramdani/bahasa-sederhana
codex plugin add bahasa-sederhana@bahasa-sederhana
```

Codex meminta Anda memercayai hook sesi sebelum hook itu berjalan pertama kali.

## Hook sesi

Hook ini membaca blok aturan dari `prompts/system-prompt.md`. Blok itu adalah teks di antara dua baris pertama yang isinya tepat `---`. Hook ini mencetak blok itu di awal sesi. Akibatnya, agen menerapkan aturan tanpa menunggu perintah Anda.

Jika berkas itu tidak ada, hook ini mencetak ringkasan aturan yang lebih pendek. Hook ini selalu keluar dengan kode 0, jadi sesi tetap berjalan.

## Hook pemeriksaan berkas

Setelah agen menulis berkas `.md`, `.mdx`, `.txt`, atau `.rst`, hook ini memeriksa berkas itu dengan `evals/bahasa_lint.py`. Berkas lain tidak diperiksa.

Hook ini memilih jenis teks dari nama berkas dan judul pertamanya. Jika nama atau judul itu menyebut runbook, panduan, pemasangan, atau pemecahan masalah, hook ini memakai batas prosedur. Batas prosedur adalah 20 kata per kalimat. Berkas lain memakai batas deskripsi, yaitu 25 kata per kalimat.

Jika berkas itu punya pelanggaran, hook ini menghentikan agen dan menampilkan daftar temuan. Daftar itu memuat paling banyak sepuluh temuan, masing-masing dengan nomor baris dan kategorinya. Lalu, agen memperbaiki berkas itu.

Hook ini melewati path berikut secara bawaan:

- Folder `.git`, `node_modules`, dan `.claude`
- Folder `skills/bahasa-sederhana/`
- Berkas `examples/sebelum-sesudah.md`

Dua path terakhir berisi contoh buruk yang disengaja.

## Hook pemeriksaan balasan

Setelah agen selesai menjawab, hook ini membaca balasan terakhir dari transkrip sesi. Hook ini menghitung tanda pisah, huruf tebal, subjudul, baris butir, kata cakapan, pembuka basa-basi, dan penutup basa-basi. Blok kode tidak dihitung.

Jika ada temuan, Claude Code menampilkan pesan singkat kepada Anda. Hook ini tidak membatasi panjang balasan dan tidak menghentikan agen.

## Mengecualikan path

Isi variabel lingkungan `BAHASA_SEDERHANA_LINT_EXCLUDE` dengan pola *glob*. Pisahkan beberapa pola dengan koma atau titik dua. Hook pemeriksaan berkas mencocokkan setiap pola dengan path lengkap, path relatif terhadap folder proyek, dan nama berkas.

```bash
export BAHASA_SEDERHANA_LINT_EXCLUDE="docs/lama/*,README.md"
```

Contoh ini melewati semua berkas di `docs/lama/` dan setiap berkas bernama `README.md`. README di repositori ini berisi contoh "Tanpa skill" yang disengaja, jadi Anda dapat melewatinya dengan cara ini. Pola `*` melewati semua berkas dan mematikan hook pemeriksaan berkas saja.

## Mematikan hook

Jika Anda ingin mematikan semua hook plugin ini di Claude Code, nonaktifkan plugin `bahasa-sederhana` lewat menu `/plugin`. Skill dan gaya keluaran plugin itu ikut nonaktif.

Jika Anda ingin mematikan semua hook dari semua plugin dan pengaturan, tulis `"disableAllHooks": true` di `~/.claude/settings.json`. Pengaturan ini juga mematikan hook lain yang Anda pasang.

Di Codex, tolak hook sesi saat Codex meminta Anda memercayainya. Anda juga dapat menghapus plugin itu dari Codex.

## Pengujian

Jalankan pengujian dari folder utama repositori:

```bash
node --test src/hooks/bahasa-sederhana-activate.test.js
python3 src/hooks/test_lint_hook.py
```

Pengujian hook sesi memakai `node:test`. Pengujian hook pemeriksaan memakai Python 3 saja. Kedua pengujian tidak membutuhkan jaringan.
