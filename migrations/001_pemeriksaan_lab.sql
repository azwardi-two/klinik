CREATE TABLE IF NOT EXISTS pemeriksaan_lab (
    id_pemeriksaan_lab INT AUTO_INCREMENT PRIMARY KEY,
    id_kunjungan INT NOT NULL,
    status VARCHAR(20) DEFAULT 'REGISTER',
    jam_mulai DATETIME NULL,
    jam_target DATETIME NULL,
    jam_selesai DATETIME NULL,
    created_by INT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pemeriksaan_lab_kunjungan
        FOREIGN KEY (id_kunjungan) REFERENCES kunjungan(id_kunjungan),
    CONSTRAINT fk_pemeriksaan_lab_user
        FOREIGN KEY (created_by) REFERENCES users(id)
);

ALTER TABLE pemeriksaan_pasien
    ADD COLUMN id_pemeriksaan_lab INT NULL AFTER id;

ALTER TABLE pemeriksaan_pasien
    ADD CONSTRAINT fk_pemeriksaan_pasien_lab
        FOREIGN KEY (id_pemeriksaan_lab) REFERENCES pemeriksaan_lab(id_pemeriksaan_lab);

INSERT INTO pemeriksaan_lab (
    id_kunjungan,
    status,
    jam_mulai,
    jam_target,
    jam_selesai,
    created_by,
    created_at
)
SELECT
    pp.id_kunjungan,
    CASE
        WHEN SUM(CASE WHEN pp.status <> 'SELESAI' THEN 1 ELSE 0 END) = 0 THEN 'SELESAI'
        WHEN SUM(CASE WHEN pp.status = 'PROSES' THEN 1 ELSE 0 END) > 0 THEN 'MULAI'
        ELSE 'REGISTER'
    END AS status,
    MIN(pp.jam_mulai) AS jam_mulai,
    MAX(pp.jam_seharusnya_selesai) AS jam_target,
    MAX(pp.jam_selesai) AS jam_selesai,
    MIN(pp.created_by) AS created_by,
    MIN(pp.created_at) AS created_at
FROM pemeriksaan_pasien pp
WHERE pp.id_pemeriksaan_lab IS NULL
GROUP BY pp.id_kunjungan;

UPDATE pemeriksaan_pasien pp
JOIN pemeriksaan_lab pl ON pl.id_kunjungan = pp.id_kunjungan
SET pp.id_pemeriksaan_lab = pl.id_pemeriksaan_lab
WHERE pp.id_pemeriksaan_lab IS NULL;
