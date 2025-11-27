from models.user import WasteInfo
from services.database import DatabaseService

db = DatabaseService()

class wasteController:
    def __init__(self):
        pass

    def load_waste_info(self):
        row = db.load_all("informasi_sampah")
        waste_info_list = []

        for item in row:
            # Schema: jenis, title, text_part, image_path
            waste_info_list.append(WasteInfo(jenis=item[0], title=item[1], text_part=item[2], image_path=item[3]))
        
        return waste_info_list
    
    def add_waste_info(self, jenis: str, title: str, text_part: str, image_path: str):
        query = "INSERT INTO informasi_sampah (jenis, title, text_part, image_path) VALUES (?, ?, ?, ?)"
        params = (jenis, title, text_part, image_path)
        db.execute_query(query, params)

    def update_waste_info(self, jenis_sampah: str, title: str, text_part: str, image_path: str):
        query = "UPDATE informasi_sampah SET title = ?, text_part = ?, image_path = ? WHERE jenis = ?"
        params = (title, text_part, image_path, jenis_sampah)
        db.execute_query(query, params)

    def delete_waste_info(self, jenis_sampah: str):
        query = "DELETE FROM informasi_sampah WHERE jenis = ?"
        params = (jenis_sampah,)
        db.execute_query(query, params)

    def search_waste_info(self, keyword: str):
        all_waste = self.load_waste_info()
        filtered = [
            waste for waste in all_waste 
            if keyword.lower() in waste.jenis.lower() 
            or keyword.lower() in waste.title.lower()
        ]
        return filtered
    
    def get_waste_by_jenis(self, jenis: str):
        query = "SELECT * FROM informasi_sampah WHERE jenis = ?"
        row = db.fetch_one(query, (jenis,))
        if row:
            return WasteInfo(jenis=row[0], title=row[1], text_part=row[2], image_path=row[3])
        return None