from sqlalchemy.orm import Session
from app.models.barang import Barang, PenerimaanBarang, PemakaianBarang
from app.repositories.barang import BarangRepository, PenerimaanBarangRepository, PemakaianBarangRepository
from app.core.uow import UnitOfWork


class BarangService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BarangRepository(db)
        self.penerimaan_repo = PenerimaanBarangRepository(db)
        self.pemakaian_repo = PemakaianBarangRepository(db)

    def create_barang(self, data):
        with UnitOfWork(self.db) as uow:
            barang = Barang(
                id_jenis_tabung=data.id_jenis_tabung,
                nama_barang=data.nama_barang,
                kategori=data.kategori or "BAHAN_PAKAI",
                satuan=data.satuan,
                harga_satuan=data.harga_satuan or 0,
                stok_minimum=data.stok_minimum or 0,
            )
            self.repo.create(barang)
            uow.flush()
            return self._response(barang)

    def update_barang(self, id_barang: int, data):
        with UnitOfWork(self.db) as uow:
            barang = self.repo.get_by_id(id_barang)
            if not barang:
                return None
            if data.id_jenis_tabung is not None:
                barang.id_jenis_tabung = data.id_jenis_tabung
            if data.nama_barang is not None:
                barang.nama_barang = data.nama_barang
            if data.kategori is not None:
                barang.kategori = data.kategori
            if data.satuan is not None:
                barang.satuan = data.satuan
            if data.harga_satuan is not None:
                barang.harga_satuan = data.harga_satuan
            if data.stok_minimum is not None:
                barang.stok_minimum = data.stok_minimum
            return self._response(barang)

    def get_barang(self, id_barang: int):
        barang = self.repo.get_by_id(id_barang)
        if not barang:
            return None
        return self._response_with_stok(barang)

    def get_all_barang(self):
        rows = self.repo.get_all()
        return [self._response_with_stok(r) for r in rows]

    def delete_barang(self, id_barang: int):
        with UnitOfWork(self.db) as uow:
            barang = self.repo.get_by_id(id_barang)
            if not barang:
                return False
            self.repo.delete(barang)
            return True

    def barang_masuk(self, id_barang: int, data):
        with UnitOfWork(self.db) as uow:
            barang = self.repo.get_by_id(id_barang)
            if not barang:
                return None
            penerimaan = PenerimaanBarang(
                id_barang=id_barang,
                jumlah=data.jumlah,
                harga_satuan=data.harga_satuan,
            )
            self.penerimaan_repo.create(penerimaan)
            return {"id": penerimaan.id, "id_barang": id_barang, "jumlah": data.jumlah, "tipe": "MASUK"}

    def barang_keluar(self, id_barang: int, data):
        with UnitOfWork(self.db) as uow:
            barang = self.repo.get_by_id(id_barang)
            if not barang:
                return None
            pemakaian = PemakaianBarang(
                id_tabung=data.id_tabung,
                id_barang=id_barang,
                jumlah_pakai=data.jumlah_pakai,
            )
            self.pemakaian_repo.create(pemakaian)
            return {"id": pemakaian.id, "id_barang": id_barang, "jumlah": data.jumlah_pakai, "tipe": "KELUAR"}

    def get_mutasi(self, id_barang: int):
        barang = self.repo.get_by_id(id_barang)
        if not barang:
            return None
        masuk = self.penerimaan_repo.get_by_barang(id_barang)
        keluar = self.pemakaian_repo.get_by_barang(id_barang)
        mutasi = []
        for m in masuk:
            mutasi.append({"id": m.id, "id_barang": id_barang, "tipe": "MASUK", "jumlah": m.jumlah, "harga_satuan": m.harga_satuan, "created_at": str(m.created_at) if m.created_at else None})
        for k in keluar:
            mutasi.append({"id": k.id, "id_barang": id_barang, "tipe": "KELUAR", "jumlah": k.jumlah_pakai, "harga_satuan": None, "created_at": str(k.created_at) if k.created_at else None})
        mutasi.sort(key=lambda x: x.get("created_at") or "")
        return mutasi

    def get_barang_with_stok_all(self):
        rows = self.repo.get_all()
        return [self._response_with_stok(r) for r in rows]

    def _hitung_stok(self, id_barang: int) -> int:
        masuk = sum(m.jumlah for m in self.penerimaan_repo.get_by_barang(id_barang))
        keluar = sum(k.jumlah_pakai for k in self.pemakaian_repo.get_by_barang(id_barang))
        return masuk - keluar

    def _response(self, barang: Barang):
        return {
            "id_barang": barang.id_barang,
            "id_jenis_tabung": barang.id_jenis_tabung,
            "nama_barang": barang.nama_barang,
            "kategori": barang.kategori,
            "satuan": barang.satuan,
            "harga_satuan": barang.harga_satuan,
            "stok_minimum": barang.stok_minimum,
        }

    def _response_with_stok(self, barang: Barang):
        r = self._response(barang)
        r["stok"] = self._hitung_stok(barang.id_barang)
        return r
