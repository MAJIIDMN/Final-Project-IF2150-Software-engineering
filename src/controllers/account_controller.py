from services.database import DatabaseService
from models.user import User, Order

class AccountController:
    _NEAREST_POINT = {
        "a": "b",
        "b": "d",
        "c": "e",
        "d": "b",
        "e": "c",
    }

    def __init__(self):
        self.db = DatabaseService() # Koneksi ke SQLite
        self.current_user = None
        self.is_logged_in = False

    def register(self, first_name, last_name, email, phone, address, password):
        print("\n--- REGISTER ---")

        role = 'client'
        username = f"{first_name}_{last_name}".lower()
        kecamatan = "default_kecamatan"

        # Membuat objek user sementara
        new_user = User(username, password, email, kecamatan, role)

        # Realisasi Query Q-017 & Q-018 dari DPPL
        query = "INSERT INTO users (id, username, password, email, role, kecamatan) VALUES (?, ?, ?, ?, ?, ?)"
        success, message = self.db.execute_query(query, (new_user.id, username, password, email, role, kecamatan))

        if success:
            print(f"Registrasi berhasil! ID Anda: {new_user.id}")
            return new_user, message
        else:
            print("Gagal: Username mungkin sudah terpakai.")
            return None, None


    def login(self, username, email, password):

        if username is not None:
            query = "SELECT id, username, password, email, role, kecamatan, point FROM users WHERE username = ? AND password = ?"
            row = self.db.fetch_one(query, (username, password))
        else:
            query = "SELECT id, username, password, email, role, kecamatan, point FROM users WHERE email = ? AND password = ?"
            row = self.db.fetch_one(query, (email, password))

        if row:
            # row = (id, username, password, email, role, kecamatan, point)
            self.current_user = User(
                username=row[1],
                password=row[2],
                email=row[3],
                phonenumber="",
                kecamatan=row[5],
                role=row[4],
                point=row[6],
                uid=row[0]
            )
            self.is_logged_in = True
            return self.current_user
        else:
            return None

    def _get_nearest_point(self, from_point):
        key = from_point.strip().lower()
        return self._NEAREST_POINT.get(key)

    def create_order(self):
        """Membuat pesanan baru (Khusus Client)."""
        if not self.is_logged_in or self.current_user.role != 'client':
            return

        print("\n--- BUAT ORDER ---")
        jenis = input("Jenis Sampah: ")
        berat = float(input("Berat (kg): "))
        from_point = input("Titik asal (a/b/c/d/e): ").strip().lower()
        nearest_point = self._get_nearest_point(from_point)
        if nearest_point:
            print(f"Titik WC terdekat dari {from_point.upper()} adalah {nearest_point.upper()}.")
        else:
            print("Titik asal tidak dikenal, lewati perhitungan titik terdekat.")
        foto = "foto_dummy.jpg"

        new_order = Order(self.current_user, jenis, berat, foto)

        # Realisasi Query Q-013 (Insert/Update Sampah)
        query = "INSERT INTO orders (id, owner_id, jenis, berat, foto_path, status) VALUES (?, ?, ?, ?, ?, ?)"
        success, message = self.db.execute_query(query, (new_order.id, new_order.owner_id, jenis, berat, foto, "Pending"))
        if success:
            print("Order berhasil disimpan ke database!")
        else:
            print(f"Gagal menyimpan order: {message}")

    def get_pending_orders(self):
        """Melihat pesanan masuk (Khusus Waste Collector)."""
        # Realisasi pengambilan data sampah (mirip Q-002 tapi konteks order)
        query = "SELECT id, jenis, berat, status FROM orders WHERE status = 'Pending'"
        rows = self.db.fetch_all(query)
        
        print(f"\n--- DAFTAR PESANAN MASUK ({len(rows)}) ---")
        for row in rows:
            print(f"ID: {row[0]} | Jenis: {row[1]} | Berat: {row[2]}kg | Status: {row[3]}")
            
            # Simulasi Assign WC (Update DB)
            if input("Ambil order ini? (y/n): ") == 'y':
                update_q = "UPDATE orders SET status = 'Assigned', wc_id = ? WHERE id = ?"
                # Realisasi Query Q-009 (Update posisi/status)
                self.db.execute_query(update_q, (self.current_user.id, row[0]))
                print("Order berhasil diambil.")

    def logout(self):
        self.current_user = None
        self.is_logged_in = False
        print("Logout berhasil.")

    def get_point(self, username:str):
        if username is None:
            return f"0"
        query = "SELECT point FROM users WHERE username = ?"
        row = self.db.fetch_one(query, (username,))
        if row:
            point = row[0]
            if point is not None:
                return point
            return f"0"
        else:
            return None

    def register_user(self, first, last, email, phonenumber, kecamatan, password, username=None, role="client"):
        if username is None:
            username = f'{first}{last}'.lower()
        new_user = User(username, password, email, phonenumber, kecamatan)
        query = "INSERT INTO users (id, username, password, email, phonenumber, role, kecamatan) VALUES (?, ?, ?, ?, ?, ?, ?)"
        success, message = self.db.execute_query(query, (new_user.id, username, password, email, phonenumber, role, kecamatan))

        return success, message
    
    def correct_vcode(self, code_input):
        verif_code = "135182"
        if (code_input == verif_code):
            return True
        else:
            return False
        

    def find_user_with_email(self, email):
        query = "SELECT * FROM users WHERE email = ?"
        row = self.db.fetch_one(query, (email,))
        uid, username, password, mail, phone, kecamatan, role, point = row
        return User(
            username=username,
            password=password,
            email=mail,
            phonenumber=phone,
            kecamatan=kecamatan,
            role=role,
            point=point,
            uid=uid,  # penting karena user dari database
        )
    
    def find_email_of_user(self, username):
        query = "SELECT email FROM users WHERE username = ?"
        row = self.db.fetch_one(query, (username,))
        
        if row:
            return row[0]   # email
        return None
            
    def change_password(self, new_pass, email):
        query = "UPDATE users SET password = ? WHERE email = ?"
        success, message = self.db.execute_query(query, (new_pass, email))
        return success, message