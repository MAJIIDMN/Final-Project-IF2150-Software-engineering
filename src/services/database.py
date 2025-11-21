import sqlite3
import pandas as pd

class DatabaseService:
    def __init__(self, db_name="src/database/growbak.db"):
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

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS hadiah (
                id TEXT PRIMARY KEY,
                namaHadiah TEXT,
                pointCost INTEGER,
                foto_path TEXT,
                stock INTEGER,
                description TEXT,
                kategori TEXT
            )
        """)

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
    
    def insert_from_csv(self, table: str, file_path: str):
        """Memasukkan data dari file CSV ke tabel tertentu."""
        df = pd.read_csv(file_path)
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['?'] * len(df.columns))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.executemany(query, df.values.tolist())
        self.conn.commit()

    def insert_to_db(self, table: str, data: dict):
        """Memasukkan satu baris data ke tabel tertentu."""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, tuple(data.values()))
        self.conn.commit()

    def delete_from_db(self, table: str, primary_key: str, pk_values: list | tuple):
        """
        Menghapus banyak baris dari tabel berdasarkan primary key.
        """
        if not isinstance(pk_values, (list, tuple)):
            raise ValueError("pk_values harus list atau tuple")
        
        placeholders = ", ".join(["?" for _ in pk_values])
        query = f"DELETE FROM {table} WHERE {primary_key} IN ({placeholders})"

        self.cursor.execute(query, pk_values)
        self.conn.commit()

    def update_from_csv(self, table: str, file_path: str, primary_key: str):
        """Memperbarui data dari file CSV ke tabel tertentu berdasarkan primary key."""
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            set_clause = ', '.join([f"{col}=?" for col in df.columns if col != primary_key])
            query = f"UPDATE {table} SET {set_clause} WHERE {primary_key}=?"
            params = [row[col] for col in df.columns if col != primary_key] + [row[primary_key]]
            self.cursor.execute(query, params)
        self.conn.commit()

    def update_db(self, table: str, data: dict, primary_key: str):
        """Memperbarui satu baris data di tabel tertentu berdasarkan primary key."""
        set_clause = ', '.join([f"{col}=?" for col in data.keys() if col != primary_key])
        query = f"UPDATE {table} SET {set_clause} WHERE {primary_key}=?"
        params = [data[col] for col in data.keys() if col != primary_key] + [data[primary_key]]
        self.cursor.execute(query, params)
        self.conn.commit()

    def close(self):
        self.conn.close()
