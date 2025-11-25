import sqlite3
import pandas as pd
import threading

usercounter = 0
ocounter = 0

class DatabaseService:
    def __init__(self, db_name="src/database/growbak.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.lock = threading.Lock()
        self.create_tables()
        query = "SELECT id FROM users WHERE id LIKE 'U%' ORDER BY id DESC LIMIT 1"
        row = self.fetch_one(query)
        global usercounter
        if not row:
            usercounter = 0
        else: 
            last_id = row[0]
            usercounter = int(last_id[1:])

        query_orders = "SELECT id FROM orders WHERE id LIKE 'O%' ORDER BY id DESC LIMIT 1"
        row_orders = self.fetch_one(query_orders)
        global ocounter
        if not row_orders:
            ocounter = 0
        else:
            last_oid = row_orders[0]
            ocounter = int(last_oid[1:])

    def create_tables(self):
        # Membuat tabel-tabel jika belum ada
        # Tabel users
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT UNIQUE,
                phonenumber TEXT UNIQUE,
                role TEXT, -- 'client', 'wc', 'admin'
                point INTEGER DEFAULT 0,
                kecamatan TEXT
            )
        """)

        # Tabel Orders
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

        # Tabel Data Kecamatan
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS kecamatan (
                id INTEGER PRIMARY KEY,
                nama TEXT,
                latitude REAL,
                longitude REAL,
                norm_latitude REAL,
                norm_longitude REAL
            )
        """)

        # Tabel Hadiah
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS hadiah (
                id TEXT PRIMARY KEY,
                namaHadiah TEXT,
                pointCost INTEGER,
                foto_path TEXT,
                stock INTEGER,
                description TEXT,
                kategori TEXT,
                color TEXT,
                size TEXT
            )
        """)

        # Update ke database
        self.conn.commit()

    def execute_query(self, query, params=()):
        # Menjalankan query
        try:
            with self.lock:
                self.cursor.execute(query, params)
                self.conn.commit()
                return True, None
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: users.username" in str(e):
                return False, "Username sudah dipakai!"
            if "UNIQUE constraint failed: users.id" in str(e):
                return False, "ID sudah ada di database!"
            if "UNIQUE constraint failed: users.email" in str(e):
                return False, "Email sudah terdaftar!"
            if "UNIQUE constraint failed: users.phonenumber" in str(e):
                return False, "Nomor ini sudah terdaftar!"
            return False, "Terjadi kesalahan database."

    def fetch_one(self, query, params=()):
        """Mengambil satu baris data (untuk Login)."""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=()):
        """Mengambil banyak baris data (untuk List Order)."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def load_all(self, table: str):
        """Mengambil seluruh baris data (untuk List Order)."""
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def update_point(self, username: str, new_point: int):
        """Memperbarui poin user."""
        query = "UPDATE users SET point = ? WHERE username = ?"
        self.cursor.execute(query, (new_point, username))
        self.conn.commit()

    def update_stock_hadiah(self, hadiah_id: str, new_stock: int):
        """Memperbarui stock hadiah."""
        query = "UPDATE hadiah SET stock = ? WHERE id = ?"
        self.cursor.execute(query, (new_stock, hadiah_id))
        self.conn.commit()
    
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

    def eksport_to_csv(self, table: str):
        """Mengekspor data dari tabel ke file CSV."""
        query = f"SELECT * FROM {table}"
        file_path = f"src/database/file/{table}_export.csv"
        df = pd.read_sql_query(query, self.conn)
        df.to_csv(file_path, index=False)

    def close(self):
        self.conn.close()