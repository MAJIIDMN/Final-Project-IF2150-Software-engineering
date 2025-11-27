from models.user import PointMartdb, User
import json
from services.database import DatabaseService

db_service = DatabaseService()

class PointMart(PointMartdb):
    def __init__(self):
        pass

    def redeem(self, user: User):
        if user.point > self.pointCost:
            user.point -= self.pointCost
            self.stock -= 1
            """Berhasil menukar hadiah"""
            return True
        else:
            """Gagal menukar hadiah, poin tidak cukup"""
            return False
        
    def restock(self, amount):
        self.stock += amount

    def generate_next_id(self):
        last_id = self.latest_id()
        if not last_id:
            return "H001"
        prefix = last_id[0]       # H
        number = int(last_id[1:]) # 1 digit numeric part
        next_number = number + 1
        return f"{prefix}{str(next_number).zfill(3)}"

    
    def latest_id(self):
        row = db_service.fetch_one("SELECT id FROM hadiah ORDER BY id DESC LIMIT 1")
        if row:
            return row[0]
        return None

    def load_hadiah(self):
        row = db_service.load_all("hadiah")
        hadiah = []

        for item in row:
            # Schema: id, namaHadiah, pointCost, foto_path, stock, description, kategori, color, size
            color_list = json.loads(item[7]) if item[7] else []
            size_list = json.loads(item[8]) if item[8] else []
            hadiah.append({"id": item[0], "name": item[1], "points": item[2], "image": item[3], "stock": item[4], "description": item[5], "category": item[6], "colors": color_list, "sizes": size_list})
        
        return hadiah
    
    def sort_by_points_up(self, hadiah_list):
        return sorted(hadiah_list, key=lambda x: x['points'])
    
    def sort_by_points_down(self, hadiah_list):
        return sorted(hadiah_list, key=lambda x: x['points'], reverse=True)
    
    def sort_by_stock_up(self, hadiah_list):
        return sorted(hadiah_list, key=lambda x: x['stock'])
    
    def sort_by_stock_down(self, hadiah_list):
        return sorted(hadiah_list, key=lambda x: x['stock'], reverse=True)
    
    def search_hadiah(self, keyword):
        all_hadiah = self.load_hadiah()
        filtered_hadiah = [hadiah for hadiah in all_hadiah if keyword.lower() in hadiah['name'].lower() or keyword.lower() in hadiah['category'].lower() or keyword.lower() in hadiah['id'].lower()]
        return filtered_hadiah
    
    def redeem_hadiah(self, username, hadiah_id: str, list_hadiah: list):   
        user_point = db_service.fetch_one("SELECT point FROM users WHERE username = ?", (username,))
        if not user_point:
            return print("User tidak ditemukan.")
        point = user_point[0]
        for hadiah in list_hadiah:
            if hadiah['id'] == hadiah_id:
                if point >= hadiah['points'] and hadiah['stock'] > 0:
                    # Kurangi poin user
                    point -= hadiah['points']
                    # Kurangi stock hadiah
                    hadiah['stock'] -= 1
                    # Update database
                    db_service.update_point(username, point)
                    db_service.update_stock_hadiah(hadiah_id, hadiah['stock'])
                    return True
                else:
                    return False
        return False
    def avail_hadiah_list(self):
        row = db_service.load_all("hadiah")
        hadiah = []

        for item in row:
            # Schema: id, namaHadiah, pointCost, foto_path, stock, description, kategori, color, size
            if item[4] > 0:  # Cek stock > 0
                color_list = json.loads(item[7]) if item[7] else []
                size_list = json.loads(item[8]) if item[8] else []
                hadiah.append({"id": item[0], "name": item[1], "points": item[2], "image": item[3], "stock": item[4], "description": item[5], "category": item[6], "colors": color_list, "sizes": size_list})
        
        return hadiah
    def non_avail_hadiah_list(self):
        row = db_service.load_all("hadiah")
        hadiah = []

        for item in row:
            # Schema: id, namaHadiah, pointCost, foto_path, stock, description, kategori, color, size
            if item[4] == 0:  # Cek stock = 0
                color_list = json.loads(item[7]) if item[7] else []
                size_list = json.loads(item[8]) if item[8] else []
                hadiah.append({"id": item[0], "name": item[1], "points": item[2], "image": item[3], "stock": item[4], "description": item[5], "category": item[6], "colors": color_list, "sizes": size_list})
        
        return hadiah
    
    def delete_hadiah(self, hadiah_id: str):
        query = "DELETE FROM hadiah WHERE id = ?"
        db_service.execute_query(query, (hadiah_id,))

    def edit_hadiah(self, hadiah_id: str, name: str, points: int, stock: int, image: str, description: str, category: str, colors: list, sizes: list):
        colors_json = json.dumps(colors)
        sizes_json = json.dumps(sizes)
        query = """
        UPDATE hadiah
        SET namaHadiah = ?, pointCost = ?, stock = ?, foto_path = ?, description = ?, kategori = ?, color = ?, size = ?
        WHERE id = ?
        """
        db_service.execute_query(query, (name, points, stock, image, description, category, colors_json, sizes_json, hadiah_id))

    def update_hadiah_detail(self, hadiah_id: str, name: str, points: int, stock: int, image: str, description: str, category: str):
        query = """
        UPDATE hadiah
        SET namaHadiah = ?, pointCost = ?, stock = ?, foto_path = ?, description = ?, kategori = ?
        WHERE id = ?
        """
        db_service.execute_query(query, (name, points, stock, image, description, category, hadiah_id))

    def add_hadiah(self, name: str, points: int, stock: int, image: str, description: str, category: str, colors: list, sizes: list):
        colors_json = json.dumps(colors)
        sizes_json = json.dumps(sizes)
        hadiah_id = self.generate_next_id()
        query = """
        INSERT INTO hadiah (id, namaHadiah, pointCost, foto_path, stock, description, kategori, color, size)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        db_service.execute_query(query, (hadiah_id, name, points, image, stock, description, category, colors_json, sizes_json))