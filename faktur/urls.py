from django.urls import path
# from .views import DetailDataView, ItemListView
from . import views

app_name = "faktur"

urlpatterns = [
    path('browse/', views.items, name='items'),
    path('items/<int:id_pembeli>/', views.itemsFaktur, name='items_faktur'),
]
