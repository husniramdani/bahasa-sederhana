# Sebelum dan sesudah

Setiap teks "Sebelum" di bawah adalah contoh gaya tulisan AI berbahasa Indonesia yang umum ditemui. Contoh ini disusun untuk *repo* ini, bukan *output* model yang direkam. Setiap teks "Sesudah" adalah isi yang sama setelah aturan Bahasa Sederhana diterapkan. Beberapa contoh "Sesudah" memakai fakta yang dianggap diberikan pengguna, misalnya jam, angka, dan penyebab. Model tidak boleh menambah fakta yang tidak ada di sumber.

Semua contoh memakai kirimlog, alat baris perintah fiktif yang membaca berkas log aplikasi dan mengirimnya ke OpenSearch.

## 1. Pengantar README (deskripsi)

Sebelum: 1 kalimat 41 kata, "adalah merupakan", "yang mana", "secara mulus", "tangguh".

> kirimlog adalah merupakan sebuah tool CLI yang dirancang untuk mengirimkan log-log aplikasi Anda ke OpenSearch, yang mana memungkinkan tim DevOps Anda untuk memonitor sistem secara real-time dan secara mulus tanpa harus repot mengonfigurasi pipeline logging yang kompleks. Dengan arsitektur yang tangguh dan efisien, kirimlog menjadi solusi ideal untuk kebutuhan observability modern.

Sesudah: kalimat terpanjang 16 kata, satu topik per paragraf.

> Alat baris perintah kirimlog membaca berkas log aplikasi dan mengirim isinya ke OpenSearch. Tim Anda dapat mencari log semua *server* di satu tempat.
>
> Alat ini membaca baris baru dari setiap berkas log, mengubah setiap baris menjadi JSON, lalu mengirimnya per kelompok. Jika pengiriman gagal, kirimlog mencoba lagi.
>
> Semua konfigurasi ada di satu berkas, `kirimlog.toml`.

## 2. Bagian pemecahan masalah (prosedur)

Sebelum: kalimat 38 kata, tanda pisah, "silakan cek", "apabila", "dll", "mungkin".

> **Connection refused.** Jika kirimlog gagal dengan error `connection refused`, silakan cek apakah OpenSearch sudah berjalan dan port 9200 bisa diakses dari server Anda — biasanya masalah ini disebabkan oleh firewall atau OpenSearch yang belum aktif. Apabila Anda menggunakan layanan terkelola (AWS, Elastic Cloud, dll), mungkin Anda perlu mengecek aturan akses jaringannya.

Sesudah: satu instruksi per kalimat, syarat di depan, satu kata untuk "periksa".

> ## Koneksi ditolak
>
> Jika kirimlog tidak dapat terhubung ke OpenSearch, kirimlog berhenti dengan `connection refused`.
>
> 1. Pastikan OpenSearch berjalan di *host* tujuan.
> 2. Pastikan *host* yang menjalankan kirimlog dapat terhubung ke *port* 9200 di *host* tujuan. Biasanya *firewall* memblokir *port* itu.
> 3. Jika Anda memakai OpenSearch terkelola, periksa aturan akses jaringan layanan itu.

## 3. Pesan kesalahan

Sebelum:

> Ups! Sepertinya terjadi masalah saat mencoba melakukan pengiriman log ke index. Mohon pastikan user Anda memiliki hak akses yang sesuai dan silahkan coba kembali beberapa saat lagi.

Sesudah:

> Pengiriman ke indeks `logs-app` gagal dengan HTTP 403.
> Pengguna `kirimlog` tidak punya izin menulis ke indeks itu.
> Minta izin `write` untuk indeks `logs-app` kepada admin OpenSearch.

## 4. Laporan insiden (deskripsi, waktu pasti)

Sebelum:

> Kami telah mengidentifikasi adanya kendala yang mungkin berdampak pada sebagian proses pengiriman log. Tim kami telah bekerja keras untuk menangani permasalahan ini dan layanan kini telah kembali normal sepenuhnya. Kami mohon maaf atas ketidaknyamanan yang terjadi.

Sesudah:

> Antara pukul 09.15 dan 09.48 WIB, 7% kelompok log gagal terkirim. Sertifikat TLS di OpenSearch sudah kedaluwarsa. Kami mengganti sertifikat itu pada pukul 09.44. Sejak pukul 09.48, semua kelompok log terkirim lagi.

## 5. Perubahan yang merusak di catatan rilis

Sebelum:

> Perlu dicatat bahwa pada versi terbaru ini kami telah melakukan perubahan nama pada field `host` yang mungkin akan berdampak pada dashboard dan query Anda, sehingga sebaiknya Anda segera menyesuaikannya agar tidak terjadi error.

Sesudah:

> Perubahan yang merusak: ganti `host` dengan `source_host` di semua *query* dan dasbor Anda. Versi 3.0 mengganti nama *field* itu.

## 6. Terjemahan dari bahasa Inggris (lokalisasi)

Sumber (bahasa Inggris):

> You should make sure that the index where logs are stored has been created beforehand, which will allow kirimlog to seamlessly send your data.

Terjemahan harfiah:

> Anda sebaiknya memastikan bahwa index di mana log disimpan telah dibuat sebelumnya, yang mana akan memungkinkan kirimlog untuk mengirim data Anda secara mulus.

Sesudah (Bahasa Sederhana):

> Buat indeks tujuan sebelum Anda menjalankan kirimlog. Jika indeks itu belum ada, kirimlog tidak dapat mengirim data.

## 7. Balasan obrolan

Sebelum:

> Tentu! Pertanyaan yang bagus. 😊 **CORS** pada dasarnya adalah mekanisme keamanan di browser — dan ya, error ini memang sering membingungkan! Berikut beberapa hal yang perlu Anda perhatikan:
>
> - Server Anda mungkin belum mengirim header yang tepat
> - Sebaiknya cek konfigurasi backend Anda
>
> Semoga membantu!

Sesudah:

> *Browser* memblokir permintaan itu karena *server* API Anda tidak mengizinkan domain situs Anda. Aturan ini bernama CORS (aturan *browser* tentang domain yang boleh memanggil sebuah API). Tambahkan domain situs Anda ke *header* `Access-Control-Allow-Origin` di *server* API. Lalu, muat ulang halaman itu.
