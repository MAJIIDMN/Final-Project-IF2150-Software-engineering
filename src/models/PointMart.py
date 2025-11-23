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

    def load_hadiah(self):
        row = db_service.load_all("hadiah")
        hadiah = []

        for item in row:
            color_list = json.loads(item[7]) if item[7] else []
            size_list = json.loads(item[8]) if item[8] else []
            hadiah.append({"id": item[0], "name": item[1], "points": item[2], "stock": item[4], "image": item[3], "description": item[5], "category": item[6], "colors": color_list, "sizes": size_list})
        
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
        filtered_hadiah = [hadiah for hadiah in all_hadiah if keyword.lower() in hadiah['name'].lower() or keyword.lower() in hadiah['category'].lower()]
        return filtered_hadiah
    
    def redeem_hadiah(self, user: User, hadiah_id: str, list_hadiah: list):
        for hadiah in list_hadiah:
            if hadiah['id'] == hadiah_id:
                if user.point >= hadiah['points'] and hadiah['stock'] > 0:
                    # Kurangi poin user
                    user.point -= hadiah['points']
                    # Kurangi stock hadiah
                    hadiah['stock'] -= 1
                    # Update database
                    db_service.execute_query("UPDATE users SET point = ? WHERE id = ?", (user.point, user.id))
                    db_service.execute_query("UPDATE hadiah SET stock = ? WHERE id = ?", (hadiah['stock'], hadiah_id))
                    return print("Redeem berhasil!")
                else:
                    return print("Redeem gagal: Poin tidak cukup atau stock habis.")
        return False