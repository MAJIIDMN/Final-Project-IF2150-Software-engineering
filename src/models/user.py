import uuid

import services.database

class User:
    def __init__(self, username, password, email, phonenumber, kecamatan, role="client", point=0, uid=None):
        global usercounter
        if uid is not None:
        # Kalau berasal dari database pakai id lama
            self.id = uid
        else: # kalau tidak ada, register
            if role == "client" or role == "wc":
                services.database.usercounter += 1
                if (services.database.usercounter > 10**6 -1):
                    print("User penuh!")
                    return
                self.id = f"U{services.database.usercounter:05d}"
            else:
                print("Role tidak sesuai!")
                return
        self.username = username
        self.password = password
        self.email = email
        self.phonenumber = phonenumber
        self.role = role
        self.point = point
        self.kecamatan = kecamatan

class Order:
    def __init__(self, owner: User, jenis, berat, foto, oid=None, status="Pending", wc_id=None):
        services.database.ocounter += 1
        if (services.database.ocounter > 10**6 -1):
            print("Order penuh!")
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