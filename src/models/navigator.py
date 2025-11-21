class Navigator:
    _KECAMATAN_CODE = {
        "coblong": "a",
        "sukajadi": "b",
        "cidadap": "c",
        "cicendo": "d",
        "lengkong": "e",
    }

    def _normalize_name(self, nama):
        return nama.strip().lower()

    def _to_code(self, nama):
        return self._KECAMATAN_CODE.get(self._normalize_name(nama))

    def _route_filename(self, start, tujuan):
        kode_start = self._to_code(start)
        kode_tujuan = self._to_code(tujuan)
        a, b = sorted([kode_start, kode_tujuan])
        return f"{a}_{b}.jpg"

    def RuteJemput(self, start, tujuan):
        return self._route_filename(start, tujuan)

    def RuteAntar(self, start, tujuan):
        return self._route_filename(start, tujuan)

    def TunjukkanSampah(self, id_sampah):
        return "tracking.png"