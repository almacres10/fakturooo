from django.urls import path
# from .views import DetailDataView, ItemListView
from . import views

app_name = "faktur"

urlpatterns = [
    path('', views.items, name='items'),
    path('browse/', views.resetItems, name='reset_items'),
    path('items/<int:id_pembeli>/', views.itemsFaktur, name='items_faktur'),
    path('items/<int:id_pembeli>/', views.download_csv, name='download_csv'),
]
