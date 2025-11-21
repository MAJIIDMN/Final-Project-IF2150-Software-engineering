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

---

**Terakhir diupdate**: 20 November 2025
