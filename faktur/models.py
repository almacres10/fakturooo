from django.db import models

# Create your models here.
class Faktur2022(models.Model):
    no_faktur = models.CharField(max_length=200)
    tgl_faktur = models.DateField(null=False)
    id_ms_th_pjk = models.CharField(max_length=200)
    npwp_penjual = models.CharField(max_length=200)
    nama_penjual = models.CharField(max_length=200)
    nama_pembeli = models.CharField(max_length=200)
    nama_barang = models.TextField(null=False)
    jml_dpp = models.IntegerField(null=False)
    jml_ppn = models.IntegerField(null=False)