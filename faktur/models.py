from django.db import models

# Create your models here.
class RekapFaktur000(models.Model):
    id_pembeli = models.AutoField(primary_key=True, null=False)
    nama_pembeli = models.CharField(max_length=255, null=True)
    alamat_pembeli = models.CharField(max_length=255, null=True)
    thpj = models.CharField(max_length=255, null=True)
    lbr_faktur = models.FloatField(null=True)
    nil_dpp = models.FloatField(null=True)
    nil_ppn = models.FloatField(null=True)

    class Meta:
        db_table = 'fp_000_rekap'

    def __str__(self):
        return self.nama_pembeli


class Faktur2022(models.Model):
    ID_PEMBELI = models.AutoField(primary_key=True, null=False)
    KD_JNS_TRX = models.CharField(max_length=2, null=True)
    ID_STS_PENGGANTI = models.CharField(max_length=2, null=True)
    NO_FAKTUR = models.CharField(max_length=13, null=True)
    TGL_APPROVAL = models.DateField(null=True)
    TGL_FAKTUR = models.DateField(null=True)
    ID_STS_FAKTUR = models.CharField(max_length=2, null=True)
    FG_UANG_MUKA = models.CharField(max_length=2, null=True)
    ID_MS_TH_PJK = models.CharField(max_length=6, null=True)
    NPWP_PENJUAL = models.CharField(max_length=15, null=True)
    NAMA_PENJUAL = models.CharField(max_length=255, null=True)
    ALAMAT_PENJUAL = models.CharField(max_length=255, null=True)
    ID_JNS_WP_PENJUAL = models.CharField(max_length=3, null=True)
    KPPADM_PENJUAL = models.CharField(max_length=3, null=True)
    KD_KLU_PENJUAL = models.CharField(max_length=5, null=True)
    NPWP_PEMBELI = models.CharField(max_length=15, null=True)
    NAMA_PEMBELI = models.CharField(max_length=255, null=True, db_index=True)
    # nama_pembeli = models.ForeignKey(RekapFaktur000, on_delete=models.CASCADE, related_name='faktur2022_entries', null=True, db_column='id_pembeli')
    ALAMAT_PEMBELI = models.CharField(max_length=255, null=True, db_index=True)
    ID_JNS_WP_PEMBELI = models.CharField(max_length=3, null=True)
    KPPADM_PEMBELI = models.CharField(max_length=3, null=True)
    KD_KLU_PEMBELI = models.CharField(max_length=5, null=True)
    ID_FP_PENGGANTI = models.CharField(max_length=20, null=True)
    JML_BARANG = models.FloatField(null=True)
    NAMA_BARANG = models.CharField(max_length=255, null=True, db_index=True)
    HARGA_SATUAN = models.FloatField(null=True)
    HARGA_TOTAL = models.FloatField(null=True)
    DISKON = models.FloatField(null=True)
    JML_DPP = models.FloatField(null=True)
    JML_PPN = models.FloatField(null=True)
    JML_PPNBM = models.FloatField(null=True)
    TARIF_PPNBM = models.FloatField(null=True)
    KODE_OBJEK = models.CharField(max_length=255, null=True)
    rekap_faktur = models.ForeignKey(RekapFaktur000, on_delete=models.CASCADE, related_name='faktur_entries', null=True, db_column='id_pembeli')


    class Meta:
        db_table = 'fp000_2022'  # Nama tabel dalam database

    def __str__(self):
        return self.NO_FAKTUR
    
class RefWilayah(models.Model):
    ID_WILAYAH = models.AutoField(primary_key=True, null=False)
    KD_WIL = models.CharField(max_length=100,null=True)
    KELURAHAN = models.CharField(max_length=100,null=True)
    KD_KECAMATAN = models.CharField(max_length=100,null=True)
    KECAMATAN = models.CharField(max_length=100,null=True)
    KD_KOTA = models.CharField(max_length=100,null=True)
    KOTA = models.CharField(max_length=100,null=True)
    KD_PROVINSI = models.CharField(max_length=100,null=True)
    PROVINSI = models.CharField(max_length=100,null=True)
    KPPADM = models.CharField(max_length=100,null=True)

    class Meta:
        db_table = 'ref_wilayah'

    def __str__(self):
        return self.KD_WIL
