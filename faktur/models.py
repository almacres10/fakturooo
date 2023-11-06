from django.db import models

# Create your models here.
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
    NAMA_PEMBELI = models.CharField(max_length=255, null=True)
    ALAMAT_PEMBELI = models.CharField(max_length=255, null=True)
    ID_JNS_WP_PEMBELI = models.CharField(max_length=3, null=True)
    KPPADM_PEMBELI = models.CharField(max_length=3, null=True)
    KD_KLU_PEMBELI = models.CharField(max_length=5, null=True)
    ID_FP_PENGGANTI = models.CharField(max_length=20, null=True)
    JML_BARANG = models.FloatField(null=True)
    NAMA_BARANG = models.CharField(max_length=255, null=True)
    HARGA_SATUAN = models.FloatField(null=True)
    HARGA_TOTAL = models.FloatField(null=True)
    DISKON = models.FloatField(null=True)
    JML_DPP = models.FloatField(null=True)
    JML_PPN = models.FloatField(null=True)
    JML_PPNBM = models.FloatField(null=True)
    TARIF_PPNBM = models.FloatField(null=True)
    KODE_OBJEK = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'fp000_detil_2022'  # Nama tabel dalam database

    def __str__(self):
        return self.NO_FAKTUR