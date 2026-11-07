# Pola untuk setiap jenis teks

Berkas ini menyebut mode dan pola untuk teks di luar dokumentasi biasa. Contoh "Sesudah" memakai fakta yang diberikan pengguna, misalnya jam dan penyebab. Jangan menambah fakta yang tidak ada di sumber. Semua contoh memakai kirimlog, alat fiktif yang mengirim log aplikasi ke OpenSearch.

## Lokalisasi dan terjemahan dari bahasa Inggris

Mode: ikuti jenis teks sumbernya. Ini kasus terpenting, karena sebagian besar dokumentasi teknis di Indonesia berasal dari teks bahasa Inggris.

- Terjemahkan makna, bukan susunan kata. Pecah kalimat Inggris yang panjang menjadi dua atau tiga kalimat.
- Buang struktur Inggris: "di mana" sebagai penghubung, "melakukan" ditambah kata benda, dan pasif bertumpuk.
- Tentukan pilihan istilah dengan `istilah-teknis.md` sebelum mulai. Lalu, pakai pilihan itu di seluruh teks.
- Ubah format angka, tanggal, dan waktu ke format Indonesia, kecuali di dalam kode.
- Ganti kata ragu ("should", "may", "might") dengan tangga modalitas di `katalog-aturan.md`.

> Sumber: You may want to restart the agent after changing the config.
> Sesudah: Mulai ulang kirimlog setelah Anda mengubah `kirimlog.toml`. Perubahan konfigurasi berlaku setelah kirimlog dimulai ulang.

## Pesan kesalahan dan keluaran CLI

Mode: prosedur. Pembaca pesan ini sedang menghadapi kegagalan dan butuh langkah berikutnya.

Pola: sebut apa yang gagal. Jika penyebabnya diketahui, sebut penyebab itu. Lalu, beri satu perintah untuk memperbaikinya. Jangan pakai "Ups" dan jangan minta maaf.

> Sebelum: Ups! Sepertinya terjadi masalah saat mencoba melakukan pengiriman log. Mohon pastikan kredensial Anda sudah dikonfigurasi dengan benar dan silahkan coba lagi.
> Sesudah: OpenSearch menolak kata sandi untuk pengguna `kirimlog` (HTTP 401). Isi `password` di `kirimlog.toml` dengan nilai yang benar. Lalu, jalankan kirimlog lagi.

## Runbook dan SOP

Mode: prosedur. Runbook dibaca saat ada gangguan, sering oleh orang yang baru bangun tidur.

- Satu langkah, satu kalimat perintah, syarat di depan.
- Taruh peringatan sebelum langkah yang berisiko.
- Tulis hasil yang harus terlihat setelah setiap langkah, agar pembaca tahu langkah itu berhasil.

> Sesudah: PERINGATAN: Jangan hapus indeks lama sebelum *snapshot* selesai. Log di indeks itu akan hilang.

## Laporan insiden dan halaman status

Mode: deskripsi, dengan jam, tanggal, dan zona waktu. Frasa seperti "kami telah mengidentifikasi kendala" tidak memberi tahu pembaca kapan masalah terjadi atau apa dampaknya.

> Sebelum: Kami telah mengidentifikasi adanya kendala yang mungkin berdampak pada sebagian proses pengiriman log.
> Sesudah: Antara pukul 09.15 dan 09.48 WIB, 7% kelompok log gagal terkirim. Sertifikat TLS di OpenSearch sudah kedaluwarsa.

Untuk hal yang belum pasti, tulis "belum diketahui". Jangan memakai "mungkin".

## Catatan rilis

Mode: deskripsi. Satu butir, satu perubahan. Untuk perubahan yang merusak, tulis perintahnya dulu, lalu alasannya.

> Sesudah: Perubahan yang merusak: ganti `host` dengan `source_host` di semua kueri dan dasbor Anda. Versi 3.0 mengganti nama *field* itu.

## Pesan *commit* dan *pull request*

Mode: judul berupa kalimat perintah, isi berupa deskripsi. Ikuti bahasa yang dipakai tim. Jika tim memakai bahasa Indonesia, mulai judul dengan kata kerja dasar: "Tambahkan", "Perbaiki", "Hapus". Hapus pembuka seperti "PR ini bertujuan untuk".

> Sesudah: Perbaiki percobaan ulang saat OpenSearch membalas HTTP 429

## Prompt sistem dan instruksi agen AI

Mode: prosedur. Agen tidak dapat bertanya balik, jadi setiap instruksi harus berdiri sendiri.

- Satu instruksi per kalimat. Agen lebih jarang melewatkan aturan yang berdiri sendiri.
- Satu kata untuk satu tindakan. Jika prompt memakai "cek" dan "periksa", agen dapat menganggapnya dua tindakan.
- Syarat di depan: "Jika tes gagal, berhenti."
- Pakai "harus", bukan "sebaiknya". Agen membaca "sebaiknya" sebagai pilihan.

## Teks antarmuka

Mode: prosedur, dengan teks yang pendek. Tombol memakai kata kerja dasar: "Simpan", "Batal", "Kirim". Label tombol dikecualikan dari batas kalimat. Keadaan kosong menyebut keadaannya, lalu langkah berikutnya.

> Sesudah: Belum ada sumber log. Tambahkan berkas log untuk mulai mengirim.

## Pesan kepada pelanggan

Mode: deskripsi, paling banyak 25 kata per kalimat. Pakai sapaan yang sama dengan produk. Ganti permintaan maaf yang panjang dengan fakta yang dibutuhkan pelanggan.

> Sebelum: Kami mohon maaf yang sebesar-besarnya atas ketidaknyamanan yang terjadi.
> Sesudah: Log Anda dari pukul 09.15 sampai 09.48 WIB tersimpan di antrean. Kami mengirim log itu setelah layanan pulih.

## Di luar cakupan

Teks pemasaran, unggahan media sosial, dan artikel opini butuh suara penulis. Bahasa Sederhana menghapus suara itu. Tulis teks itu dengan gaya Anda, dan pakai Bahasa Sederhana untuk dokumentasi yang ditautkan dari teks itu.
