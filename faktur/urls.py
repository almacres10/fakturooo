from django.urls import path
from .views import CombinedView
from . import views

app_name = "faktur"

urlpatterns = [
    path('nama/', views.items, name='items'),
    path('alamat/', views.items2, name='items2'),
    path('cari/nama', views.cariFakturNama, name='cari_faktur_nama'),
    path('cari/alamat', views.cariFakturAlamat, name='cari_faktur_alamat'),
    path('browse/', views.resetItems, name='reset_items'),
    path('items/<int:id_pembeli>/', views.itemsFaktur, name='items_faktur'),
    path('items/<int:id_pembeli>/download', views.download_csv, name='download_csv'),
    path('cari_per_wilayah/', views.form_wilayah, name='form_wilayah'),
    path('hasil_cari_per_wilayah/', views.get_wilayah, name='get_wilayah'),
    # path('download_wilayah_csv/', views.download_all_csv, name='download_all_csv'),
    path('download_wilayah_csv_kecamatan/', views.download_all_csv_kecamatan, name='download_all_csv_kecamatan')
]
