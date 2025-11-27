# GrowBak - Waste Management Application

Aplikasi desktop untuk manajemen sampah dan daur ulang berbasis Python dengan arsitektur MVC menggunakan framework Flet.

## Daftar Isi

- [Fitur](#fitur)
- [Prasyarat](#prasyarat)
- [Instalasi](#instalasi)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [Struktur Proyek](#struktur-proyek)
- [Dokumentasi](#dokumentasi)

## Fitur

- Sistem autentikasi (Login & Sign Up)
- Manajemen profil pengguna
- Dashboard interaktif
- Antarmuka pengguna yang responsif dan user-friendly

## Prasyarat

- Python 3.10 atau lebih tinggi
- pip (Python Package Installer)

## Instalasi

1. Clone repository ini:

```bash
git clone https://github.com/kevin-wirya/IF2150-2025-K01-G09-GrowBak.git
cd IF2150-2025-K01-G09-GrowBak
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Menjalankan Aplikasi

```bash
python src/main.py
```

Aplikasi akan terbuka di jendela desktop Anda.

## Struktur Proyek

```
IF2150-2025-K01-G09-GrowBak/
├── src/
│   ├── main.py              # Entry point aplikasi
│   ├── controllers/         # Logic dan business rules
│   ├── models/              # Struktur data dan database logic
│   └── views/               # UI/Frontend (Login, Sign Up, Dashboard)
├── doc/                     # Dokumentasi
├── fonts/                   # Font files (Poppins)
├── img/                     # Asset images
├── tests/                   # Unit tests
├── requirements.txt         # Dependency list
└── README.md               # File ini
```

## Arsitektur Proyek

Proyek ini menggunakan pola **MVC (Model-View-Controller)**:

- **Models**: Berisi struktur data dan business logic
- **Views**: Menampilkan interface GUI (Login, Sign Up, Dashboard)
- **Controllers**: Jembatan antara View dan Model untuk menangani logic aplikasi

## Daftar Modul yang Diimplementasi

### 1. Autentikasi & Manajemen Akun
- **Login** (`login_window.py`) - Halaman login pengguna
- **Sign Up** (`signup_window.py`) - Pendaftaran akun baru
- **Forget Password** (`forget_password_window.py`) - Lupa password
- **Verify Password** (`forget_password_verify_window.py`) - Verifikasi kode reset password
- **Reset Password** (`reset_password_window.py`) - Reset password baru
- **Profile** (`profil_window.py`) - Manajemen profil pengguna (edit email, phone, password, foto profil)

**Controller**: `account_controller.py`

---

### 2. Point Mart (Sistem Hadiah)
- **Point Mart Window** (`point_mart_window.py`) - Tampilan katalog hadiah
- **Product Detail** (`product_detail_window.py`) - Detail produk hadiah
- **Product Edit** (`product_edit_window.py`) - CRUD produk hadiah (Admin)
- **Point Mart Control** (`point_mart_control.py`) - Panel admin untuk kelola hadiah

**Model**: `PointMart.py`

---

### 3. Manajemen Order Sampah
- **Order Window** (`order_window.py`) - Halaman pemesanan pickup sampah
- **Home Window** (`home_window.py`) - Dashboard utama dengan status order

**Model**: `user.py` (class Order)

---

### 4. Informasi Sampah
- **Informasi Sampah** (`informasi_sampah_window.py`) - Edukasi tentang jenis-jenis sampah
- **Waste Edit Page** (`waste_edit_page.py`) - CRUD informasi sampah (Admin)
- **Waste Info Control** (`waste_info_control.py`) - Panel admin untuk kelola info sampah

**Model/Controller**: `waste_info.py`

---

### 5. Admin Control Panel
- **Admin Control Page** (`admin_control_page.py`) - Dashboard admin dengan navigasi ke:
  - Point Mart Management
  - Waste Information Management
  - User Management
  - Waste Collector Management

---

### 6. Komponen Reusable
- **Navbar** (`navbar.py`) - Navigation bar dengan profil foto
- **Alert** (`Alert.py`) - Dialog konfirmasi dan notifikasi
- **Point Mart Control** (`point_mart_control.py`) - Tabel manajemen hadiah
- **Waste Info Control** (`waste_info_control.py`) - Tabel manajemen info sampah

---

## Skema Basis Data

Aplikasi menggunakan **SQLite** sebagai database dengan tabel-tabel berikut:

### 1. **users**
Menyimpan data pengguna (client dan waste collector)

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| id | TEXT | PRIMARY KEY | User ID (U00001, U00002, ...) |
| username | TEXT | UNIQUE | Username untuk login |
| password | TEXT | - | Password terenkripsi |
| email | TEXT | UNIQUE | Email pengguna |
| phonenumber | TEXT | UNIQUE | Nomor telepon |
| role | TEXT | - | Role: 'client', 'wc', 'admin' |
| point | INTEGER | DEFAULT 0 | Poin yang dimiliki |
| kecamatan | TEXT | - | Kecamatan tempat tinggal |
| profile_path | TEXT | - | Path foto profil |

---

### 2. **wc** (Waste Collectors)
Data waste collector yang bertugas pickup sampah

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| id | TEXT | PRIMARY KEY | Waste Collector ID |
| name | TEXT | - | Nama waste collector |
| experience | TEXT | - | Pengalaman kerja |
| vehicle | TEXT | - | Jenis kendaraan |
| platenumber | TEXT | UNIQUE | Nomor plat kendaraan |

---

### 3. **orders**
Transaksi pickup sampah

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| id | TEXT | PRIMARY KEY | Order ID (O00001, O00002, ...) |
| owner_id | TEXT | FOREIGN KEY | ID user yang order |
| kecamatan | TEXT | - | Lokasi pickup |
| wc_id | TEXT | FOREIGN KEY | ID waste collector yang handle |
| jenis | TEXT | - | Jenis sampah (plastic, metal, dll) |
| berat | REAL | - | Berat sampah (kg) |
| foto_path | TEXT | - | Path foto sampah |
| status | TEXT | DEFAULT 'Pending' | Status: Pending/Completed |

---

### 4. **hadiah** (Rewards)
Katalog hadiah yang bisa ditukar dengan poin

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| id | TEXT | PRIMARY KEY | Hadiah ID (H001, H002, ...) |
| namaHadiah | TEXT | - | Nama produk hadiah |
| pointCost | INTEGER | - | Harga dalam poin |
| foto_path | TEXT | - | Path foto produk |
| stock | INTEGER | - | Stok tersedia |
| description | TEXT | - | Deskripsi produk |
| kategori | TEXT | - | Kategori produk |
| color | TEXT | - | Pilihan warna (JSON array) |
| size | TEXT | - | Pilihan ukuran (JSON array) |

---

### 5. **informasi_sampah**
Edukasi tentang jenis-jenis sampah

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| jenis | TEXT | PRIMARY KEY | Jenis sampah (plastic, metal, clothes) |
| title | TEXT | - | Judul artikel |
| text_part | TEXT | - | Konten edukasi |
| image_path | TEXT | - | Path gambar ilustrasi |

---

### 6. **kecamatan**
Data geografis kecamatan untuk mapping

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| id | INTEGER | PRIMARY KEY | ID kecamatan |
| nama | TEXT | - | Nama kecamatan |
| latitude | REAL | - | Koordinat latitude |
| longitude | REAL | - | Koordinat longitude |
| norm_latitude | REAL | - | Latitude ternormalisasi |
| norm_longitude | REAL | - | Longitude ternormalisasi |

---

## Pembagian Modul (Tim)

Dokumentasi pembagian tugas modul dapat dilihat di folder `doc/`.

---

**Terakhir diupdate**: 27 November 2025
