
saat ini saya mau menambahkan fitur pemeriksaan lab yang sekaligus dengan fitur biaya yang akan dibebankan serta lamanya waktu pemeriksaan diperlukan ketika dipilih oleh user .

fitur yang ingin ditambahkan , selain pemeriksaan satuan di dalam sistem juga memiliki paket pemeriksaan yang bisa terdiri dari beberapa item pemeriksaan yang biaya paket biasanya lebih murah dari paket satuan , dengan waktu pemeriksaan yang terakumulasi dari masing-masing pemeriksaan.

dan setiap pemeriksaan memiliki nilai normal yang terdiri dari jenis:  nilai range, operator value (<,>,>=,<=) dengan nilainya ,nilai text  , setiap hasil pemeriksaan memiliki nilai bawah/atas (jika range) dan nilai ( jika operator value) dan text jika text . 

dan di dalam hasil pemeriksaan detail juga tolong ditambahkan kolom nilai atas,nilai bawah yang akan mengisi jika range , dan nilai value (untuk mengisi jenis yang operator value) dan nilai text untuk jenis text  

mohon dibuatkan juga model datanya agar link antara pemeriksaan yang dipilih oleh pasien baik pemeriksaan satuan atau yang paket dapat ditrace back untuk memvalidasi keakuratan datanya 

Untuk perubahan yang melibatkan 2 atau lebih tabel mohon menggunakan uow dapat dapat commit dan rollback dalam kesatuan transaksi

system juga bisa mendapatkan kapan pemeriksaan dimulai dan selesai ,serta diberi peringatan jika seharusnya pemeriksaan sudah selesai berdasarkan jam mulai dan jam seharsunya selesai , seperti ada dashboard (ui) menunjukkan pemeriksaan yang telah lewat waktu

kita bisa menambah masing2 parameter nilai normal untuk setiap pemeriksaan berdasarkan usia (dalam hari) , jenis kelamin  ( tapi nanti minta di UI ketika mendefiniksannya tetap dalam hitungan ,bisa memilih mau dalam hari atau bulan atau tahun).walaupun di db tetap dalam hari 

dan dari hasil pemeriksaan bisa diketahui apakah nilai pemeriksaan itu L (low) , N (normal) dan High ( dengan icon tanda panah yang menunjukkan status pemeriksaan tersebut berdsarkan nilai ) 

pemeriksaan juga bisa diupdate , di mana nanti akan mengupdate summary dari pemeriksaan lab tersebut .

sistem juga bisa menampilkan tagihan atas pemeriksaan 




   
