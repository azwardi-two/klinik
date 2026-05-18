from typing import Optional
from app.models.nilai_normal import NilaiNormal
from app.repositories.nilai_normal import NilaiNormalRepository
from app.core.uow import UnitOfWork


class NilaiNormalService:
    def __init__(self, db):
        self.db = db

    def create_nilai_normal(self, data):
        with UnitOfWork(self.db) as uow:
            repo = NilaiNormalRepository(self.db)

            nilai = NilaiNormal(
                id_pemeriksaan=data.id_pemeriksaan,
                jenis_kelamin=data.jenis_kelamin,
                usia_hari_min=data.usia_hari_min or 0,
                usia_hari_max=data.usia_hari_max or 99999,
                nilai_bawah=data.nilai_bawah,
                nilai_atas=data.nilai_atas,
                operator=data.operator,
                nilai_operator=data.nilai_operator,
                nilai_text=data.nilai_text,
                keterangan=data.keterangan,
            )

            repo.create(nilai)
            uow.flush()

            return {
                "id_nilai_normal": nilai.id_nilai_normal,
                "id_pemeriksaan": nilai.id_pemeriksaan,
            }

    def get_nilai_normal(self, id_nilai_normal: int):
        repo = NilaiNormalRepository(self.db)
        n = repo.get_by_id(id_nilai_normal)
        if not n:
            return None
        return {
            "id_nilai_normal": n.id_nilai_normal,
            "id_pemeriksaan": n.id_pemeriksaan,
            "jenis_kelamin": n.jenis_kelamin,
            "usia_hari_min": n.usia_hari_min,
            "usia_hari_max": n.usia_hari_max,
            "nilai_bawah": n.nilai_bawah,
            "nilai_atas": n.nilai_atas,
            "operator": n.operator,
            "nilai_operator": n.nilai_operator,
            "nilai_text": n.nilai_text,
            "keterangan": n.keterangan,
        }

    def get_by_pemeriksaan(self, id_pemeriksaan: int):
        repo = NilaiNormalRepository(self.db)
        rows = repo.get_by_pemeriksaan(id_pemeriksaan)
        return [
            {
                "id_nilai_normal": n.id_nilai_normal,
                "id_pemeriksaan": n.id_pemeriksaan,
                "jenis_kelamin": n.jenis_kelamin,
                "usia_hari_min": n.usia_hari_min,
                "usia_hari_max": n.usia_hari_max,
                "nilai_bawah": n.nilai_bawah,
                "nilai_atas": n.nilai_atas,
                "operator": n.operator,
                "nilai_operator": n.nilai_operator,
                "nilai_text": n.nilai_text,
                "keterangan": n.keterangan,
            }
            for n in rows
        ]

    def get_all_nilai_normal(self):
        repo = NilaiNormalRepository(self.db)
        rows = repo.get_all()
        return [
            {
                "id_nilai_normal": n.id_nilai_normal,
                "id_pemeriksaan": n.id_pemeriksaan,
                "jenis_kelamin": n.jenis_kelamin,
                "usia_hari_min": n.usia_hari_min,
                "usia_hari_max": n.usia_hari_max,
                "nilai_bawah": n.nilai_bawah,
                "nilai_atas": n.nilai_atas,
                "operator": n.operator,
                "nilai_operator": n.nilai_operator,
                "nilai_text": n.nilai_text,
                "keterangan": n.keterangan,
            }
            for n in rows
        ]

    def compute_status_nilai(
        self,
        id_pemeriksaan: int,
        jenis_nilai: str,
        nilai_bawah: Optional[float] = None,
        nilai_atas: Optional[float] = None,
        nilai_value: Optional[float] = None,
        nilai_text: Optional[str] = None,
        jenis_kelamin: Optional[str] = None,
        umur_hari: Optional[int] = None,
    ):
        repo = NilaiNormalRepository(self.db)
        all_normals = repo.get_by_pemeriksaan(id_pemeriksaan)

        matched = None
        for n in all_normals:
            if n.jenis_kelamin and jenis_kelamin and n.jenis_kelamin != jenis_kelamin:
                continue
            if umur_hari is not None:
                if not (n.usia_hari_min <= umur_hari <= n.usia_hari_max):
                    continue
            matched = n
            break

        if not matched:
            return None

        if jenis_nilai == "range":
            val = nilai_value if nilai_value is not None else nilai_atas
            if val is None:
                return None
            if matched.nilai_bawah is not None and val < matched.nilai_bawah:
                return "L"
            if matched.nilai_atas is not None and val > matched.nilai_atas:
                return "H"
            return "N"

        elif jenis_nilai == "operator":
            val = nilai_value if nilai_value is not None else nilai_atas
            if val is None:
                return None
            op = matched.operator
            norm_val = matched.nilai_operator
            if op and norm_val is not None:
                if op == "<":
                    return "N" if val < norm_val else "H"
                elif op == ">":
                    return "N" if val > norm_val else "L"
                elif op == "<=":
                    return "N" if val <= norm_val else "H"
                elif op == ">=":
                    return "N" if val >= norm_val else "L"
            return None

        elif jenis_nilai == "text":
            if nilai_text is None:
                return None
            if matched.nilai_text and nilai_text.strip().lower() == matched.nilai_text.strip().lower():
                return "N"
            return "L"

        return None

    def update_nilai_normal(self, id_nilai_normal: int, data):
        with UnitOfWork(self.db) as uow:
            repo = NilaiNormalRepository(self.db)
            n = repo.get_by_id(id_nilai_normal)
            if not n:
                return None

            if data.jenis_kelamin is not None:
                n.jenis_kelamin = data.jenis_kelamin
            if data.usia_hari_min is not None:
                n.usia_hari_min = data.usia_hari_min
            if data.usia_hari_max is not None:
                n.usia_hari_max = data.usia_hari_max
            if data.nilai_bawah is not None:
                n.nilai_bawah = data.nilai_bawah
            if data.nilai_atas is not None:
                n.nilai_atas = data.nilai_atas
            if data.operator is not None:
                n.operator = data.operator
            if data.nilai_operator is not None:
                n.nilai_operator = data.nilai_operator
            if data.nilai_text is not None:
                n.nilai_text = data.nilai_text
            if data.keterangan is not None:
                n.keterangan = data.keterangan

            return {
                "id_nilai_normal": n.id_nilai_normal,
                "id_pemeriksaan": n.id_pemeriksaan,
            }

    def delete_nilai_normal(self, id_nilai_normal: int):
        with UnitOfWork(self.db) as uow:
            repo = NilaiNormalRepository(self.db)
            n = repo.get_by_id(id_nilai_normal)
            if not n:
                return False
            repo.delete(n)
            return True
