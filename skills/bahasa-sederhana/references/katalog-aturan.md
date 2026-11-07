# Katalog aturan: Bahasa Sederhana untuk teks perangkat lunak

Berkas ini dipakai untuk mode periksa, untuk Mode Baku, dan untuk kode aturan yang dipertanyakan. `SKILL.md` memuat aturan yang paling banyak mengubah keluaran. Berkas ini memuat katalog lengkapnya.

Setiap aturan punya kode BS (Bahasa Sederhana). Kolom STE menyebut aturan ASD-STE100 Issue 9 yang menjadi asal aturan itu. Tanda "baru" berarti aturan itu khusus untuk bahasa Indonesia. Aturan bertanda (B) hanya berlaku dalam Mode Baku (lihat `mode-baku.md`). Kaidah ejaan merujuk ke EYD Edisi V. Bentuk kata merujuk ke KBBI.

### Bagian 1: Kata

| Kode | STE | Aturan |
|---|---|---|
| BS1.1 | 1.1-1.4 | Pakai bentuk baku KBBI: risiko, praktik, analisis, silakan, izin, sistem. |
| BS1.2 | baru | Jangan pakai singkatan obrolan (yg, dgn, utk, tdk, krn, sdh, tsb) atau kata cakapan (gak, udah, aja, banget, bikin, pake, kalo, gimana, sih, dong). |
| BS1.3 | 1.5, 1.8 | Istilah teknis bidang Anda boleh dipakai sebagai nomina teknis ("*webhook*", "*commit*", "*endpoint*"). |
| BS1.4 | 1.7, 1.13 | Jangan mengubah kelas kata istilah teknis tanpa aturan. Kata kerja dari istilah asing memakai imbuhan dan tanda hubung (di-*deploy*), atau diganti kata kerja Indonesia. |
| BS1.5 | 1.9, 1.10 | Pilih istilah yang pendek dan jelas. Ikuti kebijakan tiga kelompok di `istilah-teknis.md`. |
| BS1.6 | 1.11 | Satu benda, satu nama. Jangan menulis "config" di satu tempat dan "pengaturan" di tempat lain. |
| BS1.7 | 1.12 | Kata kerja domain boleh dipakai ("pasang", "jalankan", "unggah"). Jika ada kata kerja umum yang sama artinya, pakai kata itu: "temukan", bukan "deteksi". |
| BS1.8 | baru | Tulis kata asing yang belum diserap dengan huruf miring pada pemakaian pertama di setiap dokumen, kecuali di dalam kode atau sebagai nama diri. |
| BS1.9 | baru | Tulis "Anda" dengan huruf kapital di semua posisi. Pilih satu sapaan untuk seluruh dokumen. |

Sebelum: Kamu bisa men-trigger webhook-nya, terus anda deploy aja servicenya.
Sesudah: Kirim peristiwa itu ke *webhook*. Lalu, *deploy* layanan itu.

### Bagian 2: Frasa nomina

| Kode | STE | Aturan |
|---|---|---|
| BS2.1 | 2.1 | Tulis frasa nomina paling banyak empat kata. Bahasa Indonesia meletakkan inti di depan, jadi frasa panjang mudah rancu. |
| BS2.2 | 2.2 | Jika istilah teknis butuh lebih dari empat kata, tulis lengkap satu kali, lalu beri bentuk pendek. |

Pecah frasa nomina panjang dengan kata depan (untuk, pada, dari):

Sebelum: batas ukuran kelompok pengiriman log aplikasi
Sesudah: batas ukuran kelompok untuk pengiriman log

### Bagian 3: Kata kerja

| Kode | STE | Aturan |
|---|---|---|
| BS3.1 | 3.2 | Bahasa Indonesia tidak punya kala. Tulis keterangan waktu yang jelas. Pakai "sudah", "belum", atau "akan" hanya jika maknanya perlu. |
| BS3.2 | 3.4 | Jangan menumpuk penanda aspek dan pasif: "telah dilakukan pemeriksaan oleh tim" menjadi "Tim memeriksa ...". |
| BS3.3 | 3.5 | Jangan menyambung anak kalimat lepas tanpa subjek setelah koma (", sehingga memudahkan", ", menjadikannya", ", memberikan"). Tulis kalimat baru dengan subjek. |
| BS3.4 | 3.6 | Langkah prosedur memakai kalimat perintah aktif. Dalam deskripsi, pasif di- boleh jika pelakunya tidak diketahui atau tidak penting. Jika pelakunya penting, sebut: "Anda" (pembaca) atau "kami" (penulis). |
| BS3.5 | 3.7 | Nyatakan tindakan dengan kata kerja, bukan "melakukan" ditambah kata benda: "kompres berkas itu", bukan "lakukan kompresi pada berkas itu". |
| BS3.6 | baru | Kalimat perintah tidak memakai "silakan" atau "mohon" sebagai pengisi. Kata itu menambah panjang tanpa menambah instruksi. |

Modalitas yang dipakai: dapat, akan, harus. Yang tidak dipakai: sebaiknya, seharusnya, hendaknya, mungkin, barangkali, bisa jadi. Tangga modalitas di akhir berkas ini memberi pengganti untuk setiap kata.

### Bagian 4: Kalimat

| Kode | STE | Aturan |
|---|---|---|
| BS4.1 | 4.1 | Tulis kalimat pendek dan jelas. |
| BS4.2 | 4.2 | Jangan menghilangkan kata tugas untuk memendekkan kalimat. Pertahankan "bahwa", "yang", "untuk", dan subjek. |
| BS4.3 | 4.3 | Pakai daftar vertikal untuk teks yang rumit: titik dua pada kalimat pengantar, butir diawali huruf kapital, titik hanya pada butir yang berupa kalimat, jangan mencampur instruksi dan fakta, jangan bersarang. |
| BS4.4 | 4.4 | Pakai kata penghubung antarkalimat ("Lalu,", "Akibatnya,", "Oleh karena itu,"). EYD V menaruh koma setelah kata penghubung antarkalimat. |
| BS4.5 | 4.5 | Jika rujukan dapat rancu, pakai "ini" atau "itu" ditambah nama benda. Jangan menumpuk "tersebut" dan "-nya". |

Aturan BS4.2 melawan gaya telegram. Bahasa sederhana adalah kalimat pendek dengan tata bahasa lengkap:

Salah: Indeks harus ada sebelum kirim.
Benar: Pastikan indeks tujuan sudah ada sebelum Anda menjalankan kirimlog.

### Bagian 5: Prosedur

| Kode | STE | Aturan |
|---|---|---|
| BS5.1 | 5.1 | Paling banyak 20 kata per kalimat, termasuk peringatan. |
| BS5.2 | 5.2 | Satu instruksi per kalimat, kecuali dua tindakan terjadi bersamaan. Sebuah langkah boleh menambah satu kalimat untuk hasil langsung atau batasan. |
| BS5.3 | 5.3 | Tulis instruksi sebagai kalimat perintah: "Hapus berkas sementara." |
| BS5.4 | 5.4 | Taruh syarat sebelum perintah, dipisah koma: "Jika tes gagal, buka laporan tes." Pakai "jika" untuk semua syarat. |
| BS5.5 | 5.5 | Catatan berisi informasi, bukan instruksi atau batasan. Batasan ditulis bersama tindakannya. Uji catatan: prosedur harus tetap berjalan jika semua catatan dihapus. |

Sebelum: Kamu perlu bikin user khusus di OpenSearch dulu sebelum isi config, yang mana bisa dilakukan lewat Dashboards.
Sesudah: Buat pengguna `kirimlog` di OpenSearch Dashboards. Lalu, tulis nama pengguna itu di `kirimlog.toml`.

### Bagian 6: Deskripsi

| Kode | STE | Aturan |
|---|---|---|
| BS6.1 | 6.1 | Beri informasi bertahap: satu fakta baru per kalimat. |
| BS6.2 | 6.2 | Pakai kata kunci untuk membuat struktur yang logis. |
| BS6.3 | 6.3 | Paling banyak 25 kata per kalimat. |
| BS6.4 | 6.4 | Kelompokkan informasi yang berkaitan dalam paragraf. |
| BS6.5 | 6.5 | Satu topik per paragraf. |
| BS6.6 | 6.6 | Paling banyak enam kalimat per paragraf. |

### Bagian 7: Peringatan keselamatan

| Kode | STE | Aturan |
|---|---|---|
| BS7.1 | 7.1 | Pakai kata yang menunjukkan tingkat risiko: PERINGATAN untuk cedera atau kehilangan data, PERHATIAN untuk kerusakan. Jika keduanya terjadi, pakai PERINGATAN. |
| BS7.2 | 7.2 | Mulai dengan perintah atau syarat yang jelas. |
| BS7.3 | 7.3 | Lalu, sebut risikonya atau akibat yang dapat terjadi. |

Taruh instruksi sebelum penjelasan. Pola yang sama berlaku untuk flag CLI yang merusak dan migrasi yang tidak dapat dibatalkan.

Sebelum: Perlu diperhatikan bahwa log lama mungkin saja ikut terhapus apabila flag --hapus-lama dipakai sebelum proses snapshot benar-benar selesai.
Sesudah: PERINGATAN: Jangan pakai flag `--hapus-lama` sebelum *snapshot* selesai. Flag itu menghapus indeks lama beserta isinya.

### Bagian 8: Tanda baca dan angka

| Kode | STE | Aturan |
|---|---|---|
| BS8.1 | 8.1 | Jangan pakai titik koma. Tulis dua kalimat. |
| BS8.2 | 8.2 | Pakai tanda hubung untuk kata ulang (anak-anak) dan untuk imbuhan pada kata asing (di-*deploy*). |
| BS8.3 | 8.3 | Tanda kurung boleh untuk rujukan, singkatan, penjelasan istilah, dan pilihan. |
| BS8.4 | 8.4 | Dalam daftar vertikal, titik dua pada kalimat pengantar mengakhiri kalimat itu. Setiap butir dihitung sebagai kalimat baru. |
| BS8.5 | 8.5-8.7 | Hitung sebagai satu kata: teks dalam kurung, kata ulang, angka, angka dengan satuan, singkatan, identifier, teks kutipan, judul, label, dan nama diri. |
| BS8.6 | baru | Pakai koma untuk desimal dan titik untuk ribuan dalam prosa: 12,5%, 1.500 baris, Rp15.000. Angka dalam kode dan nomor versi tidak berubah. |
| BS8.7 | baru | Tulis waktu dengan titik dan zona waktu: pukul 02.30 UTC, pukul 09.30 WIB. Tulis tanggal sebagai 7 November 2026. |
| BS8.8 | baru | Ganti singkatan dll., dsb., dst., e.g., dan i.e. Sebut butirnya, atau pakai "misalnya" dan "yaitu". |

Aturan BS8.5 penting untuk teks perangkat lunak. `kirimlog kirim --config kirimlog.toml` di dalam tanda petik terbalik dihitung satu kata.

Tanda pisah (aturan skill ini, bukan aturan EYD): tanda pisah (`—`) di antara dua pernyataan menyembunyikan hubungan logisnya. Sebut hubungannya ("karena", "tetapi", "misalnya"), atau tulis dua kalimat. Tanda hubung berspasi atau tanda hubung ganda di antara pernyataan sama dengan tanda pisah. Rentang angka (`5–10`), penanda daftar, dan flag (`--force`) bukan tanda pisah.

### Bagian 9: Praktik menulis

| Kode | STE | Aturan |
|---|---|---|
| BS9.1 | 9.1 | Jika penggantian kata per kata tidak berhasil, susun ulang kalimatnya. |
| BS9.2 | 9.2 | Pakai setiap kata dengan makna dan kelas kata yang benar. "Daripada" untuk membandingkan, bukan pengganti "dari". |
| BS9.3 | 9.3 | Pilih kata kerja tunggal yang jelas, bukan ungkapan panjang: "turun", bukan "mengalami penurunan". |
| BS9.4 | 9.4 | Pertahankan gaya dan istilah yang sama di seluruh dokumen. |
| BS9.5 | baru | Jangan meniru struktur bahasa Inggris. "Di mana" dan "yang mana" hanya untuk pertanyaan. Sebagai penghubung, pakai "tempat", "yang", "saat", atau kalimat baru. |
| BS9.6 | baru | Hapus pleonasme: "adalah merupakan", "agar supaya", "demi untuk", "sangat ... sekali", "para pengguna-pengguna", "naik ke atas". |
| BS9.7 | baru | "Kami" berarti penulis tanpa pembaca. "Kita" berarti penulis bersama pembaca. Dokumentasi produk biasanya memakai "kami". |

Sebelum: Server di mana aplikasi berjalan adalah merupakan server yang mana dikelola oleh tim infra.
Sesudah: Tim infrastruktur mengelola *server* tempat aplikasi berjalan.

### Bagian 10: Ciri tulisan AI

Tulisan AI punya ciri yang mudah dikenali. Aturan di atas sudah menghapus sebagian. Cegah sisanya, di dokumen dan di balasan:

| Kode | Ciri | Tindakan |
|---|---|---|
| BS10.1 | Pembuka umum: "Di era digital saat ini", "Dalam dunia yang terus berkembang" | Hapus. Mulai dengan fakta. |
| BS10.2 | Pentingnya dibesar-besarkan: "krusial", "memainkan peran penting", "kunci utama" | Nyatakan faktanya. |
| BS10.3 | Paralelisme negatif: "tidak hanya X, tetapi juga Y" | Tulis X dan Y sebagai dua fakta. |
| BS10.4 | Tiga serangkai hiasan: "cepat, aman, dan andal" | Sebut sifat yang dapat diukur, atau hapus. |
| BS10.5 | Sumber kabur: "studi menunjukkan", "banyak ahli berpendapat" | Sebut sumbernya, atau hapus klaimnya. |
| BS10.6 | Rentang palsu: "mulai dari X hingga Y" tanpa batas nyata | Sebut butirnya. |
| BS10.7 | Ringkasan ulang: "Kesimpulannya", "Secara keseluruhan" | Hapus paragraf itu. |
| BS10.8 | Sisipan opini: "perlu dicatat bahwa", "penting untuk diingat" | Hapus, lalu nyatakan faktanya. |
| BS10.9 | Sisa percakapan: "Semoga membantu", "Jangan ragu untuk bertanya" | Hapus. |
| BS10.10 | Kebiasaan format: huruf tebal sebagai hiasan, emoji sebagai struktur, subjudul untuk dua kalimat | Hapus formatnya. |

Untuk kata-kata yang sering dipakai berlebihan, `padanan-kata.md` memetakan setiap kata ke pengganti sederhana. Jika kata itu tidak membawa fakta, hapus kata itu.

### Tangga modalitas

| Anda menulis | Tulis ini |
|---|---|
| sebaiknya, seharusnya, hendaknya (wajib) | harus |
| sebaiknya (saran) | "Kami menyarankan X karena Y.", atau tulis sebagai fakta: "X lebih cepat karena Y." |
| seandainya, jika sampai | jika |
| mungkin, barangkali, bisa jadi (kemungkinan) | Sebut syaratnya ("Jika X terjadi, Y gagal"), pakai "dapat" untuk peristiwa ("unggahan dapat gagal"), atau tulis "kadang-kadang" atau "belum diketahui". |
| boleh, bisa (izin) | dapat |
| perlu, wajib, diharuskan | harus, atau kalimat perintah dalam prosedur |

## Pilihan kata

Satu kata, satu makna, satu kelas kata, untuk seluruh dokumen (BS1.6, BS9.4):

| Konsep | Kata yang dipakai | Jangan berganti dengan |
|---|---|---|
| melihat sesuatu | periksa | cek, verifikasi, konfirmasi |
| menjamin keadaan | pastikan | memastikan bahwa, konfirmasi |
| berkas konfigurasi | konfigurasi | config |
| menu pengguna | pengaturan | setelan, settings |
| syarat | jika | apabila, bila, kalau, seandainya |
| kegagalan program | kesalahan | error, galat |
| sapaan | Anda (atau kamu, pilih satu) | campuran Anda dan kamu, anda |

Pengganti umum: dikarenakan → karena, melakukan instalasi → memasang, mengalami kegagalan → gagal, saat ini → hapus jika tidak membawa fakta.
