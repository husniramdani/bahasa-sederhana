# Catatan perubahan

Setiap entri menyebut versi dan tanggal. Jika ada efek terukur, entri juga menyebutnya.

## 1.1.0, 7 November 2026

- Diubah: istilah pemrograman (*script*, *output*, *push*, *repo*, *commit*, *deploy*, dan lainnya) tetap dalam bahasa Inggris. Padanan yang jarang dipakai *developer*, misalnya "skrip", "keluaran", dan "mendorong", tidak dipakai lagi dalam Mode Sederhana.
- Diubah: setiap kata Inggris ditulis miring setiap kali muncul, di dokumen dan di balasan obrolan.
- Ditambahkan: dua kategori *linter*, `istilah_tegak` dan `padanan_janggal`, dengan daftar kata di `evals/istilah_inggris.tsv` dan `evals/padanan_janggal.tsv`.
- Ditambahkan: opsi `--mode baku` pada *linter*. Opsi ini mematikan pemeriksaan `padanan_janggal`.
- Ditambahkan: dua contoh baru di `examples/sebelum-sesudah.md`, untuk istilah pemrograman di dokumen dan di balasan obrolan.
- Ditambahkan: *workflow* CI di `.github/workflows/check.yml` yang menjalankan tiga rangkaian tes pada setiap *push* dan *pull request*.

## 1.0.0, 7 November 2026

- Rilis pertama.
- Ditambahkan: `skills/bahasa-sederhana/SKILL.md` dengan dua ragam, Dokumen (15 aturan) dan Balasan (6 aturan).
- Ditambahkan: lima berkas rujukan, yaitu katalog aturan bernomor BS, Mode Baku, padanan kata, kebijakan istilah teknis, dan kasus penggunaan.
- Ditambahkan: aturan STE yang disesuaikan untuk bahasa Indonesia. Aturan kala diganti keterangan waktu. Larangan pasif diganti larangan pasif bertumpuk. Aturan artikel diganti aturan kata tugas. Aturan kontraksi diganti aturan kata cakapan.
- Ditambahkan: aturan khusus bahasa Indonesia untuk ejaan EYD V, format angka, sapaan, struktur terjemahan dari bahasa Inggris, pleonasme, dan istilah teknis.
- Ditambahkan: `evals/bahasa_lint.py` dengan 14 kategori pelanggaran, `evals/slop.tsv`, dan `evals/nonbaku.tsv`.
- Ditambahkan: *hook* sesi, *hook* pemeriksaan berkas, dan *hook* pemeriksaan balasan. Variabel lingkungan pengecualiannya bernama `BAHASA_SEDERHANA_LINT_EXCLUDE`.
- Belum ada *benchmark* untuk rilis ini.
