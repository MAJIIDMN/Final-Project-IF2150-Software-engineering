import uuid

import services.database

class User:
    def __init__(self, username, password, email, phonenumber, kecamatan, role="client", point=0, uid=None, profile_path=""):
        global usercounter
        if uid is not None:
        # Kalau berasal dari database pakai id lama
            self.id = uid
        else: # kalau tidak ada, register
            if role == "client" or role == "wc":
                services.database.usercounter += 1
                if (services.database.usercounter > 10**6 -1):
                    return
                self.id = f"U{services.database.usercounter:05d}"
            else:
                return
        self.username = username
        self.password = password
        self.email = email
        self.phonenumber = phonenumber
        self.role = role
        self.point = point
        self.kecamatan = kecamatan
        self.profile_path = profile_path

class Order:
    def __init__(self, owner: User, jenis, berat, foto, oid=None, status="Pending", wc_id=None):
        if oid is not None:
            self.id = oid
        else:
            global ocounter
            services.database.ocounter += 1
            if (services.database.ocounter > 10**6 -1):
                return
            else:
                self.id = f"O{services.database.ocounter:05d}"
        self.owner_id = owner.id
        self.kecamatan = owner.kecamatan 
        self.jenis = jenis
        self.berat = berat
        self.foto = foto
        self.status = status
        self.wc_id = wc_id

class PointMartdb:
    def __init__(self, idHadiah, namaHadiah, pointCost, stock, foto_path="", description="", kategori=""):
        self.id = idHadiah
        self.namaHadiah = namaHadiah
        self.pointCost = pointCost
        self.stock = stock
        self.foto_path = foto_path
        self.description = description
        self.kategori = kategori

class WasteInfo:
    def __init__(self, jenis, title, text_part, image_path=""):
        self.jenis = jenis
        self.title = title
        self.text_part = text_part
        self.image_path = image_path
