# Generated by Django 4.2.7 on 2023-11-27 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RefWilayah',
            fields=[
                ('ID_WILAYAH', models.AutoField(primary_key=True, serialize=False)),
                ('KD_WIL', models.CharField(max_length=100, null=True)),
                ('KELURAHAN', models.CharField(max_length=100, null=True)),
                ('KD_KECAMATAN', models.CharField(max_length=100, null=True)),
                ('KECAMATAN', models.CharField(max_length=100, null=True)),
                ('KD_KOTA', models.CharField(max_length=100, null=True)),
                ('KOTA', models.CharField(max_length=100, null=True)),
                ('KD_PROVINSI', models.CharField(max_length=100, null=True)),
                ('PROVINSI', models.CharField(max_length=100, null=True)),
                ('KPPADM', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'ref_wilayah',
            },
        ),
        migrations.CreateModel(
            name='RekapFaktur000',
            fields=[
                ('id_pembeli', models.AutoField(primary_key=True, serialize=False)),
                ('nama_pembeli', models.CharField(max_length=255, null=True)),
                ('alamat_pembeli', models.CharField(max_length=255, null=True)),
                ('thpj', models.CharField(max_length=255, null=True)),
                ('lbr_faktur', models.FloatField(null=True)),
                ('nil_dpp', models.FloatField(null=True)),
                ('nil_ppn', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'fp_000_rekap',
            },
        ),
        migrations.CreateModel(
            name='Faktur2022',
            fields=[
                ('ID_PEMBELI', models.AutoField(primary_key=True, serialize=False)),
                ('KD_JNS_TRX', models.CharField(max_length=2, null=True)),
                ('ID_STS_PENGGANTI', models.CharField(max_length=2, null=True)),
                ('NO_FAKTUR', models.CharField(max_length=13, null=True)),
                ('TGL_APPROVAL', models.DateField(null=True)),
                ('TGL_FAKTUR', models.DateField(null=True)),
                ('ID_STS_FAKTUR', models.CharField(max_length=2, null=True)),
                ('FG_UANG_MUKA', models.CharField(max_length=2, null=True)),
                ('ID_MS_TH_PJK', models.CharField(max_length=6, null=True)),
                ('NPWP_PENJUAL', models.CharField(max_length=15, null=True)),
                ('NAMA_PENJUAL', models.CharField(max_length=255, null=True)),
                ('ALAMAT_PENJUAL', models.CharField(max_length=255, null=True)),
                ('ID_JNS_WP_PENJUAL', models.CharField(max_length=3, null=True)),
                ('KPPADM_PENJUAL', models.CharField(max_length=3, null=True)),
                ('KD_KLU_PENJUAL', models.CharField(max_length=5, null=True)),
                ('NPWP_PEMBELI', models.CharField(max_length=15, null=True)),
                ('NAMA_PEMBELI', models.CharField(max_length=255, null=True)),
                ('ALAMAT_PEMBELI', models.CharField(max_length=255, null=True)),
                ('ID_JNS_WP_PEMBELI', models.CharField(max_length=3, null=True)),
                ('KPPADM_PEMBELI', models.CharField(max_length=3, null=True)),
                ('KD_KLU_PEMBELI', models.CharField(max_length=5, null=True)),
                ('ID_FP_PENGGANTI', models.CharField(max_length=20, null=True)),
                ('JML_BARANG', models.FloatField(null=True)),
                ('NAMA_BARANG', models.CharField(max_length=255, null=True)),
                ('HARGA_SATUAN', models.FloatField(null=True)),
                ('HARGA_TOTAL', models.FloatField(null=True)),
                ('DISKON', models.FloatField(null=True)),
                ('JML_DPP', models.FloatField(null=True)),
                ('JML_PPN', models.FloatField(null=True)),
                ('JML_PPNBM', models.FloatField(null=True)),
                ('TARIF_PPNBM', models.FloatField(null=True)),
                ('KODE_OBJEK', models.CharField(max_length=255, null=True)),
                ('rekap_faktur', models.ForeignKey(db_column='id_pembeli', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faktur_entries', to='faktur.rekapfaktur000')),
            ],
            options={
                'db_table': 'fp000_2022',
            },
        ),
    ]
