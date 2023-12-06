    // Mendeteksi kembali ke halaman
    window.addEventListener('pageshow', function (event) {
        // event.persisted akan true jika kembali dari cache (misalnya tombol "Back" pada browser)
        if (event.persisted) {
            // Sembunyikan loader
            document.getElementById("loader").style.display = "none";
        }
    });

    document.getElementById("buttonSubmit").addEventListener("click", function () {
        // Tampilkan loader
        document.getElementById("loader").style.display = "block";
        
        // Sediakan kode lain yang ingin Anda jalankan saat tombol diklik
        // ...

        // Formulir akan tetap terkirim karena jenis tombolnya adalah "submit"
    });