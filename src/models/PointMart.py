from user import pointMartdb, User

class PointMart(pointMartdb):
    def __init__(self, idHadiah, namaHadiah, pointCost, stock, foto_path="", description="", kategori=""):
        super().__init__(idHadiah, namaHadiah, pointCost, stock, foto_path, description, kategori)

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