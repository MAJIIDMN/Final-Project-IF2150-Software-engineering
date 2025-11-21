import sqlite3

class DatabaseService:
    def __init__(self, db_name="growbak.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Membuat tabel jika belum ada (DDL)."""
        # Tabel Users (Menggabungkan Client, WC, Admin dengan kolom 'role')
        # Merealisasikan penyimpanan untuk User Management [DPPL 2.3]
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT,
                role TEXT, -- 'client', 'wc', 'admin'
                point INTEGER DEFAULT 0,
                kecamatan TEXT
            )
        """)

        # Tabel Orders (Sampah)
        # Merealisasikan penyimpanan data sampah [DPPL Q-013, Q-014]
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                owner_id TEXT,
                kecamatan TEXT,
                wc_id TEXT,
                jenis TEXT,
                berat REAL,
                foto_path TEXT,
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY(owner_id) REFERENCES users(id),
                FOREIGN KEY(wc_id) REFERENCES users(id)
            )
        """)

        # # Data untuk kecamatan
        # self.cursor.execute("""
        #     CREATE TABLE kecamatan (
        #         id INTEGER PRIMARY KEY,
        #         nama TEXT,
        #         latitude REAL,
        #         longitude REAL,
        #         norm_latitude REAL,
        #         norm_longitude REAL
        #     )
        # """)

        self.conn.commit()

    def execute_query(self, query, params=()):
        """Menjalankan query INSERT/UPDATE/DELETE."""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Database Error: {e}")
            return False

    def fetch_one(self, query, params=()):
        """Mengambil satu baris data (untuk Login)."""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=()):
        """Mengambil banyak baris data (untuk List Order)."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()