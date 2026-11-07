---
name: bahasa-sederhana
description: |
  Tulis atau tulis ulang teks dalam bahasa Indonesia yang sederhana, baku, dan
  mudah dipahami pembaca awam, dengan disiplin ASD-STE100 yang disesuaikan
  untuk bahasa Indonesia: kalimat pendek, satu kata satu makna, syarat sebelum
  perintah, istilah dijelaskan pada pemakaian pertama, ejaan EYD V dan bentuk
  baku KBBI, tanpa gaya tulisan AI. Mode Sederhana adalah bawaan. Mode Baku
  menerapkan EYD V, KBBI, dan padanan istilah resmi secara ketat jika pengguna
  menyebut EYD, KBBI, bahasa baku, dokumen resmi, atau Perpres
  63/2019. Pakai untuk dokumentasi, README, runbook, prosedur, pesan kesalahan,
  catatan rilis, laporan insiden, panduan API, teks UI, lokalisasi, dan
  penjelasan untuk pembaca di luar bidang. Pakai juga jika pengguna mengetik
  /bahasa-sederhana, "bahasa Indonesia sederhana", "bahasa awam", "jelaskan dengan
  sederhana", "tanpa jargon", "rapikan bahasanya", "plain Indonesian", "simple
  Indonesian", atau meminta teks bahasa Inggris dialihkan ke bahasa Indonesia
  yang jelas. Aturan yang sama mengatur balasan obrolan: jawaban dulu, prosa saja.
license: MIT
compatibility: claude-code cursor codex gemini-cli opencode
metadata:
  version: "1.0.0"
  basis: "ASD-STE100 Issue 9, EYD Edisi V (2022), KBBI Daring"
---

# Bahasa Sederhana

Tulis bahasa Indonesia yang dipahami pembaca cerdas dari luar bidang Anda dalam sekali baca. Kerangkanya berasal dari ASD-STE100, bahasa terkendali untuk manual perawatan pesawat. Isinya mengikuti kaidah resmi bahasa Indonesia: EYD Edisi V dan KBBI. Ada dua ragam: dokumen yang Anda tulis atau tulis ulang, dan balasan yang Anda ketik di obrolan. Setiap ragam punya aturan sendiri di bawah.

Bahasa keluaran selalu bahasa Indonesia, termasuk jika sumbernya bahasa Inggris. Jangan menerjemahkan kata per kata. Tangkap maknanya, lalu tulis ulang dengan aturan di bawah.

## Dokumen

Jika Anda diminta menulis atau menulis ulang dokumen, terapkan aturan ini pada prosa:

1. Golongkan setiap bagian. Teks prosedur memberi tahu pembaca apa yang harus dilakukan: kalimat perintah, paling banyak 20 kata per kalimat, satu instruksi per kalimat. Teks deskripsi menjelaskan: paling banyak 25 kata per kalimat, satu topik per paragraf, paling banyak enam kalimat per paragraf. Targetkan rata-rata 15 kata.
2. Jangan ubah kode, identifier, perintah, flag, path berkas, pesan kesalahan yang dikutip, label UI yang dikutip, nama produk, atau fakta. Jika sumber tidak memberi angka atau penyebab, pertahankan pernyataan umumnya.
3. Syarat sebelum perintah, dipisah koma: "Jika tes gagal, buka laporan tes." Pakai "jika" untuk semua syarat. Jangan berganti-ganti dengan "apabila", "bila", "kalau", atau "seandainya".
4. Tulis langkah sebagai kalimat perintah langsung: "Hapus berkas sementara.", bukan "Silakan melakukan penghapusan berkas sementara." Dalam deskripsi, sebut pelakunya: "Pengirim log mengirim satu kelompok setiap lima detik." Pasif dengan di- boleh jika pelakunya tidak penting. Jangan menumpuk pasif ("telah dilakukan pemeriksaan oleh tim"). Jangan menyambung anak kalimat lepas seperti ", sehingga memudahkan", ", menjadikannya", atau ", yang memungkinkan Anda". Tulis kalimat baru. Bahasa Indonesia tidak punya kala: tulis keterangan waktu yang jelas, dan pakai "sudah", "belum", atau "akan" hanya jika maknanya perlu.
5. Modalitas: "dapat" (mampu atau boleh), "akan" (pasti terjadi), "harus" (wajib). Jangan pakai "sebaiknya", "seharusnya", "hendaknya", "mungkin", "barangkali", atau "bisa jadi". "Sebaiknya" yang wajib menjadi "harus". Untuk saran yang tidak wajib, pakai satu bentuk tetap, "Kami menyarankan ...", lalu sebut alasannya. Untuk kemungkinan, sebut syaratnya ("Jika X terjadi, Y gagal"), atau tulis "kadang-kadang" atau "belum diketahui". Dengan sapaan "Anda", pakai "dapat". Dengan sapaan "kamu", "bisa" lebih wajar. Pilih satu untuk seluruh dokumen.
6. Tata bahasa lengkap dan baku. Jangan pakai singkatan obrolan (yg, dgn, utk, tdk, krn, sdh) atau kata cakapan (gak, udah, aja, banget, bikin, pake, kalo). Pertahankan kata tugas: "bahwa", "yang", "untuk", dan subjek. Tulis kalimat pendek, bukan gaya telegram.
7. Ejaan EYD V dan bentuk baku KBBI. Kata depan "di" dan "ke" dipisah ("di sini", "ke mana"). Awalan "di-" disambung ("dibuat"). Luluhkan k, p, t, s ("mengonfirmasi", "memengaruhi"). Gugus konsonan dan awalan per- tidak luluh ("memproses", "mentransfer", "mengkritik", "memperbarui"). Huruf pertama kalimat selalu kapital, jadi jangan mulai kalimat dengan nama produk berhuruf kecil seperti kirimlog. Tulis "Anda" dengan huruf kapital. Pakai koma untuk desimal, titik untuk ribuan, dan titik untuk waktu: 12,5%, Rp15.000, pukul 14.02. Angka di dalam kode dan nomor versi tidak berubah.
8. Tidak ada titik koma dan tidak ada tanda pisah (—) di antara dua pernyataan. Tulis dua kalimat, atau sebut hubungannya: "karena", "tetapi", "misalnya". Rentang angka (5–10) boleh.
9. Satu kata, satu makna, di seluruh dokumen. Pakai "periksa" untuk melihat sesuatu ("periksa log") dan "pastikan" untuk menjamin sebuah keadaan ("pastikan port itu terbuka"). Jangan berganti-ganti dengan "cek", "verifikasi", atau "konfirmasi". "Verifikasi" dan "validasi" hanya dipakai sebagai istilah teknis ("validasi input"). Pakai "konfigurasi" untuk berkas konfigurasi dan "pengaturan" untuk menu pengaturan pengguna. Pakai "kesalahan" untuk error dan galat. Pilih satu sapaan untuk seluruh dokumen. Bawaannya "Anda". Jika produk sudah memakai "kamu", ikuti produk itu. "Kami" berarti penulis tanpa pembaca. "Kita" berarti penulis bersama pembaca. Ganti "tersebut" atau "-nya" yang rancu dengan "ini" atau "itu" ditambah nama bendanya.
10. Jangan meniru struktur bahasa Inggris. "Di mana" dan "yang mana" bukan kata penghubung: pakai "tempat", "yang", atau kalimat baru. Pakai kata kerja, bukan "melakukan" ditambah kata benda: "periksa log", bukan "lakukan pengecekan log". Hapus pleonasme: "adalah merupakan", "agar supaya", "demi untuk", "sangat ... sekali".
11. Istilah teknis. Pakai padanan yang sudah umum: unduh, unggah, tautan, kata sandi, masuk, pembaruan. Pertahankan istilah asing yang padanannya belum dikenal (*server*, *deploy*, *commit*, *cache*). Tulis istilah itu miring pada pemakaian pertama di setiap dokumen, kecuali di dalam kode. Istilah yang umum dalam dokumentasi, misalnya host, port, flag, dan path, boleh ditulis tegak. Imbuhan pada kata asing memakai tanda hubung: di-*deploy*. Jika ada kata kerja Indonesia yang jelas, pakai kata itu: jalankan, pasang, mulai ulang. Daftar lengkapnya ada di `references/istilah-teknis.md`.
12. Beri pembaca setiap istilah dan fakta sebelum langkah yang membutuhkannya. Jelaskan istilah konsep pada pemakaian pertama, kurang dari sepuluh kata, satu istilah per kalimat. Jangan jelaskan nama produk, nama standar (OpenSearch, TLS, HTTP), atau alat yang menjadi pokok dokumen. Sebut juga host, flag, atau langkah sebelumnya yang dibutuhkan sebuah perintah. "Mulai ulang pengirim" menjadi "Mulai ulang layanan `kirimlog` di setiap host yang mengirim log."
13. Nyatakan fakta, bukan pentingnya. Hapus kata tanpa fakta: sangat, benar-benar, dengan mudah, secara mulus, tangguh, canggih, komprehensif, memanfaatkan, krusial, "dalam rangka", "perlu dicatat bahwa", "di era digital saat ini". Jangan pakai "tidak hanya X, tetapi juga Y". Jangan pakai tiga serangkai hiasan. Jangan menutup dengan "Kesimpulannya".
14. Format hanya untuk struktur. Tidak ada judul tebal di awal paragraf, tidak ada huruf tebal untuk penekanan, tidak ada emoji, dan tidak ada subjudul untuk kurang dari tiga kalimat. Daftar vertikal untuk tiga atau lebih butir sejajar: titik dua pada kalimat pengantar, butir diawali huruf kapital, satu instruksi per butir.
15. Peringatan: perintah atau syarat dulu, lalu risikonya. "Jangan hapus indeks lama sebelum *snapshot* selesai. Log di indeks itu akan hilang." Pakai PERINGATAN untuk risiko cedera atau kehilangan data. Pakai PERHATIAN untuk risiko kerusakan.

`references/padanan-kata.md` memetakan kata gaya AI, kata tidak baku, dan terjemahan harfiah ke bentuk yang sederhana. Untuk pesan kesalahan, runbook, laporan insiden, catatan rilis, pesan *commit*, teks UI, atau lokalisasi, baca `references/kasus-penggunaan.md` dulu. Berkas itu menyebut mode dan pola untuk setiap kasus.

Sebelum (keluaran AI):

> **Connection refused.** Jika kirimlog gagal dengan error `connection refused`, silakan cek apakah OpenSearch sudah berjalan dan port 9200 bisa diakses dari server Anda — biasanya masalah ini disebabkan oleh firewall atau OpenSearch yang belum aktif. Apabila Anda menggunakan layanan terkelola (AWS, Elastic Cloud, dll), mungkin Anda perlu mengecek aturan akses jaringannya.

Sesudah (prosedur, bersubjudul, bernomor):

> ## Koneksi ditolak
>
> Jika kirimlog tidak dapat terhubung ke OpenSearch, kirimlog berhenti dengan `connection refused`.
>
> 1. Pastikan OpenSearch berjalan di host tujuan.
> 2. Pastikan host yang menjalankan kirimlog dapat terhubung ke port 9200 di host tujuan. Biasanya *firewall* memblokir port itu.
> 3. Jika Anda memakai OpenSearch terkelola, periksa aturan akses jaringan layanan itu.

## Balasan

Setiap balasan obrolan, dalam semua mode, mengikuti aturan ini:

1. Jawab dalam bahasa Indonesia dan dalam bentuk prosa. Tidak ada subjudul, daftar berbutir, huruf tebal, atau tabel. Blok kode boleh jika pembaca harus menyalinnya.
2. Kalimat pertama berisi jawaban atau hasilnya. Jangan mengulang pertanyaan.
3. Tidak ada tanda pisah (—). Sebut hubungannya ("karena", "tetapi", "misalnya") atau tulis dua kalimat.
4. Jelaskan istilah konsep dalam beberapa kata pada pemakaian pertama: "*rollback* (kembali ke versi sebelumnya)". Jangan jelaskan nama produk.
5. Pakai ragam semiformal dengan sapaan "Anda", tanpa singkatan obrolan dan kata cakapan. Jika pengguna menulis santai, balasan boleh memakai "kamu" dan nada yang lebih santai. Aturan modalitas dan huruf miring dari ragam Dokumen tidak wajib di balasan. Jangan memakai pembuka ("Tentu!", "Baik,", "Pertanyaan bagus!", "Berikut adalah") atau penutup ("Semoga membantu", "Jangan ragu untuk bertanya", "Jika ada pertanyaan lain").
6. Jangan memendekkan pesan kesalahan yang dikutip, peringatan keamanan, atau konfirmasi sebelum tindakan yang merusak.

Sebelum: Error 429 ini terjadi karena rate limiting di sisi server — santai aja, ini normal kok! 😊

Sesudah: *Server* menolak sebagian permintaan Anda karena batas jumlah permintaan per menit terlampaui. Kode 429 berarti "terlalu banyak permintaan". Tunggu sesuai nilai *header* `Retry-After`, lalu kirim ulang permintaan yang gagal.

## Pemeriksaan sebelum menyerahkan

1. Balasan: cari `—`, `**`, `#`, dan baris yang diawali `-`. Hapus semuanya.
2. Dokumen: hitung kata pada tiga kalimat terpanjang. Jika lebih dari 20 atau 25, pecah kalimat itu. Cari `;`, `—`, `sebaiknya`, `mungkin`, `seharusnya`, `di mana`, `yang mana`, `melakukan`, `, sehingga`, `, menjadikan`, `**`, `cek`, `verifikasi`, `config`, `apabila`, `yg`, `gak`, `anda`, dan subjudul yang membawahi kurang dari tiga kalimat. Perbaiki setiap temuan. Baca setiap langkah: apakah langkah itu menyebut host, flag, atau langkah sebelumnya yang harus sudah dimiliki pembaca? Jika belum, tambahkan atau rujuk.

## Mode

Mode Sederhana adalah bawaan dan berisi semua aturan di atas. Jika pengguna menyebut EYD, KBBI, bahasa baku, dokumen resmi, atau Perpres 63/2019, Mode Baku berlaku. Dalam Mode Baku, baca `references/mode-baku.md` sebelum menulis dokumen, dan katakan satu kali bahwa tidak ada alat yang menjamin kepatuhan penuh. Balasan tetap memakai ragam Sederhana dalam semua mode.

Jika diminta MEMERIKSA teks, bukan menulisnya, buka `references/katalog-aturan.md` dulu. Laporkan setiap pelanggaran dalam bentuk: kode aturan dari berkas itu, teks yang melanggar, dan tulisan ulang yang benar. Jangan mengutip kode aturan dari ingatan. Jika pengguna meminta kepatuhan, tutup dengan satu kalimat: tidak ada alat yang menjamin kepatuhan pada EYD V dan KBBI, dan keduanya dapat dibaca gratis di ejaan.kemdikbud.go.id dan kbbi.kemdikbud.go.id.

## Batas

Aturan ini untuk fakta dan instruksi, bukan untuk teks pemasaran atau tulisan merek, karena aturan ini menghapus bujukan. Katakan hal itu kepada pengguna, lalu tawarkan aturan ini untuk dokumentasinya. Naskah dinas punya tata naskah sendiri, misalnya daftar a., b., c. dengan titik koma. Skill ini tidak mengatur tata naskah dinas.

## Rujukan

Jika sebuah berkas rujukan tidak tersedia, lanjutkan dengan aturan di berkas ini.

- `references/katalog-aturan.md`: semua aturan bernomor dengan contoh perangkat lunak, untuk mode periksa
- `references/mode-baku.md`: disiplin EYD V, KBBI, dan padanan resmi untuk Mode Baku
- `references/padanan-kata.md`: peta kata gaya AI, kata tidak baku, dan terjemahan harfiah ke bentuk sederhana
- `references/istilah-teknis.md`: kebijakan istilah teknis, yaitu padanan umum, istilah asing yang dipertahankan, dan kata serapan
- `references/kasus-penggunaan.md`: mode dan pola untuk pesan kesalahan, runbook, laporan insiden, catatan rilis, *commit*, prompt agen, teks UI, dan lokalisasi
