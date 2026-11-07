# Kebijakan istilah teknis

Jika Anda ragu memilih istilah Inggris atau padanan Indonesia, baca berkas ini. Pembaca harus memahami istilah itu dalam sekali baca. Pembaca dokumentasi teknis adalah *developer*, dan *developer* Indonesia memakai istilah pemrograman dalam bahasa Inggris setiap hari. Padanan Indonesia yang tidak dipakai *developer* membuat teks lebih sulit dibaca, bukan lebih mudah.

Bahasa Sederhana membagi istilah menjadi tiga kelompok. Daftar di bawah adalah contoh, bukan daftar lengkap. *Linter* memakai daftar lengkap di `evals/istilah_inggris.tsv` dan `evals/padanan_janggal.tsv`.

## Kelompok A: istilah pemrograman dalam bahasa Inggris

Pakai istilah Inggris aslinya. Tulis setiap istilah ini dengan huruf miring, setiap kali muncul, di dokumen dan di balasan obrolan. Pengecualiannya hanya teks di dalam kode, nama produk, dan label UI yang dikutip.

| Pakai | Jangan pakai |
|---|---|
| *script* | "skrip" |
| *output*, *input* | "keluaran", "masukan" |
| *push*, *pull*, *fetch*, *clone* | "mendorong", "menarik" |
| *repo*, *repository* | "repositori" |
| *commit*, *branch*, *merge*, *rebase* | "cabang", "menggabungkan cabang" |
| *pull request*, *issue* | |
| *deploy*, *build*, *rollback* | "penyebaran" |
| *bug*, *debug* | "pepijat", "awakutu" |
| *server*, *cache*, *browser* | "peladen", "tembolok", "peramban" |
| *cluster*, *container*, *pod*, *instance*, *job* | |
| *endpoint*, *webhook*, *payload*, *header* | "titik akhir", "kait web" |
| *framework*, *library*, *package*, *dependency* | "kerangka kerja", "pustaka", "dependensi" |
| *runtime*, *backend*, *frontend*, *middleware* | |
| *query*, *batch*, *snapshot*, *timestamp* | "kueri" |
| *host*, *port*, *flag*, *path*, *environment variable* | |
| *hook*, *plugin*, *linter*, *benchmark*, *skill*, *prompt* | "pengait", "pengaya" |
| *firewall*, *email*, *bucket* | |

Jika istilah kelompok A dipakai sebagai kata kerja dengan imbuhan, pakai tanda hubung sesuai EYD V dan miringkan bagian Inggrisnya: di-*deploy*, men-*deploy*, di-*push*, di-*merge*. Jangan menulis "dideploy" atau "mendeploy".

Dalam kalimat perintah, istilah Inggris dipakai tanpa imbuhan: "*Push* *commit* Anda ke *branch* `main`."

## Kelompok B: padanan Indonesia yang sudah umum

Padanan ini dipakai di antarmuka dan percakapan sehari-hari. Tulis dengan huruf tegak.

| Inggris | Indonesia |
|---|---|
| download, upload | unduh, unggah |
| link | tautan |
| password | kata sandi |
| user, username | pengguna, nama pengguna |
| log in, log out | masuk, keluar |
| update | pembaruan, perbarui |
| save, delete, copy, paste, cancel | simpan, hapus, salin, tempel, batal |
| file | berkas |
| database | basis data |
| error | kesalahan |
| request, response | permintaan, respons |
| timeout | batas waktu (nilai), waktu habis (peristiwa) |
| retry | coba lagi |
| queue | antrean |
| restart | mulai ulang |
| run | jalankan |
| install | pasang, atau instal |
| config | konfigurasi |
| settings | pengaturan |
| screenshot | tangkapan layar |

## Kelompok C: kata serapan

Kata ini sudah diserap dan tercatat di KBBI. Tulis dengan huruf tegak dan ejaan Indonesia.

aplikasi, data, fitur, kode, sistem, versi, proses, memori, program, protokol, instalasi, direktori, parameter, variabel, fungsi, modul, migrasi, sinkronisasi, autentikasi, otorisasi, enkripsi, dokumentasi, dasbor, rilis, log, klien, token, indeks, agen.

## Aturan pakai

1. Satu istilah, satu bentuk. Jika Anda memilih *repo*, jangan menulis *repository* di bagian lain dokumen yang sama.
2. Miringkan setiap istilah Inggris, setiap kali muncul. *Linter* melaporkan istilah Inggris yang tidak miring sebagai `istilah_tegak`.
3. Jelaskan istilah konsep kelompok A pada pemakaian pertama, kurang dari sepuluh kata: "*cache* (salinan data sementara untuk mempercepat baca)". Istilah alur kerja yang sudah umum, misalnya *commit* dan *push*, tidak perlu dijelaskan.
4. Nama produk, nama perintah, dan label UI tidak diterjemahkan dan tidak dimiringkan. Tulis label UI persis seperti di layar, di dalam tanda petik terbalik: klik `Save`.
5. Singkatan teknis umum (API, URL, HTTP, CLI, SQL, CI) tidak dijelaskan dan tidak dimiringkan.
6. Jangan menyerap istilah secara asal: "mengupdate", "mendownload", dan "diinstall" bukan bentuk baku. Tulis "memperbarui", "mengunduh", dan "dipasang" atau "diinstal".

## Mode Baku

Mode Baku tetap memakai padanan resmi dari KBBI dan Pasti, karena dokumen resmi wajib memakai bahasa Indonesia jika padanannya ada. Tulis istilah Inggris dalam kurung dan huruf miring pada pemakaian pertama: "peladen (*server*)", "tembolok (*cache*)", "skrip (*script*)". *Linter* tidak melaporkan `padanan_janggal` jika dijalankan dengan `--mode baku`.
