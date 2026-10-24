# Task 5 — Identity dan pengiriman pesan dengan Reticulum

Program pada `send_message.py` memakai satu file untuk dua peran:

- **Node B** membuat `RNS.Identity`, membuat destination `IN/SINGLE`, lalu
  mendaftarkan request handler bernama `message`. Saat request diterima, Node B
  menampilkan pesan di terminal dan mengirim konfirmasi kembali.
- **Node A** menerima destination hash Node B, mencari identity yang diumumkan
  di jaringan, membuat `Link`, kemudian mengirim payload melalui `Link.request`.

Identity Node B dibuat saat program dijalankan. Karena itu, gunakan destination
hash yang tercetak pada sesi Node B yang sedang aktif.

## Persiapan

1. Pastikan Python sudah terpasang.
2. Buka PowerShell atau terminal pada folder `week6\Task5`.
3. Pasang Reticulum bila belum tersedia:

   ```powershell
   py -m pip install rns
   ```

## Menjalankan dua node

Buka **dua terminal** pada folder `week6\Task5`.

Di terminal pertama jalankan penerima:

```powershell
py send_message.py node-b
```

Tunggu sampai Node B menampilkan `Destination hash`, lalu salin hash tersebut.
Di terminal kedua, ganti `<HASH_NODE_B>` dengan hash yang disalin:

```powershell
py send_message.py node-a <HASH_NODE_B> --message "Halo Node B, ini pesan dari Node A!"
```

Node B akan mencetak isi pesan, sementara Node A menampilkan konfirmasi
penerimaan. Untuk mengirim pesan lain, jalankan lagi perintah Node A dengan
teks berbeda. Hentikan Node B dengan `Ctrl+C`.

Kedua proses harus bisa berkomunikasi melalui jaringan Reticulum yang sama.
Pada dua komputer, pastikan keduanya mempunyai interface Reticulum yang saling
terhubung dan dapat bertukar announcement; destination hash saja tidak
menghubungkan perangkat yang berada di jaringan terpisah.

Contoh indikator hasil yang diharapkan:

```text
[Node B] Destination hash: <hash hexadecimal>
[Node B] Pesan diterima!
[Node B] Isi pesan: Halo Node B, ini pesan dari Node A!
[Node A] Konfirmasi: Pesan berhasil diterima oleh Node B.
[Node A] Pesan berhasil dikirim.
```