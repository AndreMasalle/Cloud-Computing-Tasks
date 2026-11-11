## 2.a. Problem Statement

**Introduction of the Problem:**
Pemilik bisnis e-commerce skala kecil hingga menengah (SME) seringkali mengandalkan spreadsheet manual atau catatan terpisah untuk mencatat produk, pelanggan, dan transaksi penjualan harian. Ketika volume transaksi meningkat, metode manual ini menjadi tidak efisien dan rentan terhadap kesalahan pencatatan. 

**Why it is important to be addressed:**
Tanpa sistem yang terpusat, pemilik bisnis kesulitan mendapatkan insight secara real-time. Mereka tidak dapat dengan cepat mengetahui produk mana yang paling menguntungkan, siapa pelanggan paling loyal (yang menghabiskan uang paling banyak), dan berapa total pendapatan kumulatif saat ini. Keterlambatan dalam menganalisis data ini dapat menyebabkan hilangnya peluang bisnis, seperti gagal melakukan restock pada produk yang sedang laris atau tidak memberikan apresiasi yang tepat kepada pelanggan setia.

**How to address it:**
Untuk mengatasi masalah ini, dibangun sebuah aplikasi web **"E-Commerce Analytics System"**. Aplikasi ini menyediakan antarmuka (Frontend) yang memungkinkan pemilik toko mengelola data Produk, Pelanggan, dan Pesanan secara mudah. Di sisi Backend (FastAPI), aplikasi ini secara otomatis mengalkulasi data tersebut untuk menghasilkan Dashboard interaktif, peringkat 5 Pelanggan Teratas berdasarkan total belanja, dan peringkat 5 Produk Terlaris berdasarkan pendapatan, sehingga pengambilan keputusan bisnis dapat dilakukan secara cepat dan akurat.

---

## 2.b. Application Requirements & Entities

Aplikasi ini memenuhi seluruh kriteria:
*   **CRUD Operations**: Setiap entitas (Products, Customers, Orders) memiliki API untuk Create, Read, Update, dan Delete.
*   **Minimum 3 Entities**: Memiliki 3 entitas utama yaitu `Products`, `Customers`, dan `Orders`.
*   **No Database**: Data disimpan sementara menggunakan tipe data Dictionary (`Dict`) Python di dalam memori (in-memory storage), tanpa menggunakan RDBMS (MySQL/PostgreSQL) atau NoSQL. Data awal di-hardcode melalui fitur seeding di frontend yang memanggil API.
*   **Frontend & Backend**: Backend menggunakan **FastAPI** (Python) dan Frontend menggunakan **HTML/CSS/JavaScript** murni dengan desain UI modern.

### 2.b.1. Table of Features (10 Points)

| Feature | Description | Entity Involved |
| :--- | :--- | :--- |
| **Manage Products** | Pengguna dapat menambahkan, melihat, mengubah, dan menghapus data produk (nama, kategori, harga, stok). | `Products` |
| **Manage Customers** | Pengguna dapat mendaftarkan pelanggan baru, melihat daftar pelanggan, mengubah data (termasuk tingkat membership Bronze, Silver, Gold, dan Platinum), dan menghapusnya. | `Customers` |
| **Manage Orders** | Pengguna dapat membuat, melihat, mengubah, dan menghapus pesanan (memilih pelanggan, produk, dan jumlah). Sistem otomatis menghitung ulang total harga setiap kali pesanan dibuat atau diubah. | `Orders`, `Products`, `Customers` *(Multi-Entity)* |
| **Dashboard Summary** | Menampilkan total pendapatan, total pesanan, rata-rata nilai pesanan, daftar pesanan terbaru, dan peringatan stok menipis secara real-time. | `Orders`, `Products`, `Customers` *(Multi-Entity)* |
| **Top Products Analytics** | Fitur backend yang mengagregasi data pesanan untuk menghitung pendapatan dan kuantitas terjual per produk, lalu menampilkan 5 produk dengan pendapatan tertinggi dalam bentuk bar chart yang berwarna sesuai kategori produk. | `Orders`, `Products` *(Multi-Entity)* |
| **Top Products Analytics** | Fitur backend yang mengagregasi data pesanan untuk menampilkan 5 produk dengan pendapatan dan kuantitas terjual tertinggi dalam bentuk bar chart yang berwarna sesuai kategori produk. | `Orders`, `Products` *(Multi-Entity)* |
| **Sales Analytics Charts** | Halaman Analitik menampilkan grafik tren pendapatan kumulatif, bubble chart harga vs jumlah terjual, pendapatan per kategori, dan pendapatan per membership. | `Orders`, `Products`, `Customers` *(Multi-Entity)* |

*(Catatan: Fitur yang melibatkan 2 entitas atau lebih sudah terpenuhi pada fitur Manage Orders, Dashboard Summary, Top Customers/Products Analytics, dan Sales Analytics Charts).*

### 2.b.2   