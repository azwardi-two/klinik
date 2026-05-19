-- Migration: Tabel profil klinik
-- Jalankan setelah aplikasi di-restart agar SQLAlchemy create_all membuat tabel

CREATE TABLE IF NOT EXISTS klinik (
    id_klinik   INT PRIMARY KEY AUTO_INCREMENT,
    nama        VARCHAR(200) NOT NULL DEFAULT 'Klinik',
    alamat      TEXT,
    telepon     VARCHAR(50),
    logo        VARCHAR(255)
);

INSERT INTO klinik (nama, alamat, telepon)
SELECT 'Klinik Sehat', 'Jl. Alternatif No. 123, Jakarta', '021-123456'
WHERE NOT EXISTS (SELECT 1 FROM klinik);
