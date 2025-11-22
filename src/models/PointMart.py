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