-- Migration: Pindahkan jenis_nilai ke tabel pemeriksaan, tambah satuan
-- Jalankan setelah aplikasi di-restart agar SQLAlchemy create_all menambah kolom baru

-- 1. Tambah kolom jenis_nilai dan satuan di tabel pemeriksaan
ALTER TABLE pemeriksaan
    ADD COLUMN jenis_nilai VARCHAR(10) NOT NULL DEFAULT 'range',
    ADD COLUMN satuan VARCHAR(50) DEFAULT NULL;

-- 2. Update jenis_nilai di pemeriksaan berdasarkan data nilai_normal yang ada
--    (ambil jenis_nilai dari salah satu nilai_normal untuk tiap pemeriksaan)
UPDATE pemeriksaan p
    JOIN (
        SELECT id_pemeriksaan, jenis_nilai
        FROM nilai_normal
        GROUP BY id_pemeriksaan, jenis_nilai
    ) n ON p.id_pemeriksaan = n.id_pemeriksaan
SET p.jenis_nilai = n.jenis_nilai;

-- 3. Hapus kolom jenis_nilai dari tabel nilai_normal
ALTER TABLE nilai_normal DROP COLUMN jenis_nilai;
