Perbaikan fiturlab UI

1. dashboard , bukan per/setiap pemeriksaan tetapi berdasarkan kunjungan dengan data yang ditampilkan sudah betul (per kunjungan). jika secara keseluruhan pemeriksaan waktu telah terlewati maka diset ini sudah melewati batas waktu  

Aturan mulai dan selesai ,sebagai berikut : 
karena setiap kunjungan memiliki data jam mulai yang sama untuk setiap pemeriksaan ketika diklik tombol hanya untuk kunjungan tersebut dimulai , dan pemeriksaan yang sudah diinput hasilnya maka berikan indikator flag di pemeriksaan_pasien bahwa sudah selesai. 

2.di tabel pemeriksaan_pasien langsung berisi pemeriksaan detail ,bagaimana jika desain untuk pemeriksaan_detail memiliki  master pemeriksaan_lab , yang berisi id_pemeriksaan_lab,id_kunjungan,status (register,mulai,selesai) , jam_mulai, jam_target,jam_selesai . dan jika jam sekarang > jam target dan status <>'selesai' maka ini yang menjadi dasar  kunjungan yang terlambat dalam pemeriksaan labnya












