from django.urls import path
from .views import DataListView
from . import views

app_name = "faktur"

urlpatterns = [
    path('', views.items, name='items'),
    path('browse/', views.resetItems, name='reset_items'),
    path('items/<int:id_pembeli>/', views.itemsFaktur, name='items_faktur'),
    path('items/<int:id_pembeli>/download', views.download_csv, name='download_csv'),
    # path('per_wilayah/', views.perWilayah, name='per_wilayah'),
    path('per_wilayah/', DataListView.as_view(), name='per_wilayah')
]
