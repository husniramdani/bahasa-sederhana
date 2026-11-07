# Uji tekanan manual

Berkas ini berisi enam skenario untuk menguji Bahasa Sederhana secara manual. Setiap skenario memakai kirimlog, alat baris perintah fiktif yang membaca berkas log aplikasi dan mengirimnya ke OpenSearch. Uji tekanan memeriksa apakah agen tetap mengikuti aturan saat permintaan pengguna mendorong ke arah lain.

## Cara menjalankan

1. Pasang *skill* atau *plugin* Bahasa Sederhana di agen yang diuji.
2. Buka sesi baru untuk setiap skenario.
3. Salin *prompt* skenario itu apa adanya ke sesi baru.
4. Periksa jawaban agen dengan daftar periksa skenario itu.
5. Catat hasilnya di baris "Hasil tercatat" pada skenario itu. Tulis nama agen, model, tanggal, dan butir yang gagal.

Untuk jawaban berupa dokumen, Anda juga dapat menjalankan *linter*:

```bash
python3 evals/bahasa_lint.py --type procedural jawaban.md
```

Hasil *linter* hanya pelengkap. Daftar periksa tetap menjadi acuan utama.

## Skenario 1: Tugas dokumentasi tanpa nama *skill*

Skenario ini menguji apakah *skill* aktif untuk permintaan dokumentasi biasa. *Prompt* tidak menyebut nama *skill* dan tidak meminta bahasa sederhana.

*Prompt*:

```text
bikinin bagian troubleshooting buat README kirimlog dong. kasusnya connection refused ke OpenSearch port 9200 sama HTTP 401 karena password di kirimlog.toml salah
```

Daftar periksa:

- Jawaban memakai bahasa Indonesia baku, bukan gaya obrolan pengguna.
- Setiap langkah berupa kalimat perintah dengan paling banyak 20 kata.
- Syarat berada di depan perintah dan selalu memakai "jika".
- Pesan `connection refused` ditulis persis di dalam kode.
- Jawaban tidak memakai "sebaiknya", "mungkin", "cek", atau "apabila".
- Jawaban tidak memakai titik koma, tanda pisah, atau huruf tebal sebagai hiasan.

Hasil tercatat: Belum ada.

## Skenario 2: Pemeriksaan dengan kode aturan

Skenario ini menguji mode periksa. Agen harus melaporkan setiap pelanggaran dengan kode aturan dari katalog.

*Prompt*:

```text
/bahasa-sederhana periksa teks ini dan sebut kode aturannya:

kirimlog adalah merupakan tool yg dirancang untuk mengirim log ke OpenSearch secara mulus, sehingga memudahkan tim. Apabila koneksi gagal, kamu sebaiknya cek config di mana alamat server ditulis; lalu jalankan ulang.
```

Daftar periksa:

- Agen membuka `references/katalog-aturan.md` sebelum menjawab.
- Setiap temuan memuat kode BS, teks yang melanggar, dan tulisan ulang yang benar.
- Semua kode yang dipakai ada di katalog.
- Contohnya BS1.2 untuk "yg", BS3.3 untuk anak kalimat lepas, dan BS8.1 untuk titik koma.
- Contoh lainnya BS9.5 untuk "di mana" dan BS9.6 untuk "adalah merupakan".
- Tulisan ulang memakai kalimat pendek, syarat di depan dengan "jika", dan tanpa titik koma.

Hasil tercatat: Belum ada.

## Skenario 3: Tekanan "sesingkat mungkin"

Skenario ini menguji aturan BS4.2. Pengguna meminta teks sesingkat mungkin dengan singkatan, tetapi tata bahasa harus tetap lengkap.

*Prompt*:

```text
tulis runbook hapus indeks lama kirimlog sesingkat mungkin ya, pake singkatan aja biar cepet dibaca on-call. intinya snapshot dulu baru hapus
```

Daftar periksa:

- Kalimatnya pendek, tetapi subjek dan kata tugas tetap ada.
- Jawaban tidak memakai singkatan obrolan seperti "yg", "utk", atau "dgn".
- Langkah membuat *snapshot* muncul sebelum langkah menghapus indeks.
- PERINGATAN muncul sebelum langkah menghapus, karena log di indeks lama dapat hilang.
- Peringatan itu menyebut perintah dulu, lalu risikonya.

Hasil tercatat: Belum ada.

## Skenario 4: Permintaan halaman pemasaran

Skenario ini menguji batas *skill*. Teks pemasaran berada di luar cakupan Bahasa Sederhana.

*Prompt*:

```text
/bahasa-sederhana bikinin copy landing page kirimlog yang catchy dan bikin orang pengen langsung install
```

Daftar periksa:

- Agen mengatakan bahwa aturan ini untuk fakta dan instruksi, bukan untuk teks pemasaran.
- Agen menawarkan aturan ini untuk dokumentasi yang ditautkan dari halaman itu, misalnya README.
- Agen tidak menulis teks pemasaran dengan gaya Bahasa Sederhana tanpa menyebut batas ini.
- Jika agen tetap menulis teks pemasaran atas permintaan pengguna, agen menyebut bahwa aturan ini tidak dipakai untuk teks itu.

Hasil tercatat: Belum ada.

## Skenario 5: Pesan kesalahan

Skenario ini menguji pola pesan kesalahan dari `references/kasus-penggunaan.md`. Pesan harus menyebut apa yang gagal, penyebabnya, dan satu langkah perbaikan.

*Prompt*:

```text
bikinin pesan error kirimlog buat HTTP 403 pas ngirim ke index logs-app. penyebabnya user kirimlog gak punya izin write ke index itu
```

Daftar periksa:

- Kalimat pertama menyebut kegagalan pengiriman ke indeks `logs-app` dengan HTTP 403.
- Pesan menyebut penyebabnya: pengguna `kirimlog` tidak punya izin menulis ke indeks itu.
- Pesan memberi satu langkah perbaikan, misalnya meminta izin `write` kepada admin OpenSearch.
- Pesan tidak memakai "Ups", permintaan maaf, "silakan", atau "mohon".
- Nama indeks dan kode HTTP tidak berubah.

Hasil tercatat: Belum ada.

## Skenario 6: Terjemahan dari bahasa Inggris

Skenario ini menguji terjemahan makna. Sumbernya bahasa Inggris dengan struktur yang mudah diterjemahkan kata per kata.

*Prompt*:

```text
terjemahin ke bahasa indonesia buat docs kirimlog: "You should ensure that the index where logs are stored has been created beforehand, which will allow kirimlog to seamlessly send your data. In order to avoid errors, perform a verification of kirimlog.toml."
```

Daftar periksa:

- Hasilnya menerjemahkan makna, bukan susunan kata.
- Hasilnya tidak memakai "di mana" atau "yang mana" sebagai penghubung.
- Hasilnya tidak memakai "melakukan" ditambah kata benda, misalnya "melakukan verifikasi".
- Hasilnya tidak memakai "dalam rangka", "secara mulus", atau "memungkinkan".
- Frasa "should ensure" menjadi kalimat perintah atau "harus", bukan "sebaiknya".
- Kalimat Inggris yang panjang dipecah menjadi dua kalimat atau lebih.

Hasil tercatat: Belum ada.
