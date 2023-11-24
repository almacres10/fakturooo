from django.urls import path
# from .views import DetailDataView, ItemListView
from . import views

app_name = "faktur"

urlpatterns = [
    path('browse/', views.items, name='items'),
    path('items/<str:nama_pembeli>/', views.itemsFaktur, name='items_faktur'),
]
