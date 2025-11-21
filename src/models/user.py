import uuid

class User:
    def __init__(self, username, password, email, kecamatan, role="client", uid=None, point=0):
        self.id = uid if uid else str(uuid.uuid4())[:8]
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.point = point
        self.kecamatan = kecamatan

class Order:
    def __init__(self, owner: User, jenis, berat, foto, oid=None, status="Pending", wc_id=None):
        self.id = oid if oid else str(uuid.uuid4())[:8]
        self.owner_id = owner.id
        self.kecamatan = owner.kecamatan   # <<< ambil dari user
        self.jenis = jenis
        self.berat = berat
        self.foto = foto
        self.status = status
        self.wc_id = wc_id
