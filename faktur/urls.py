from django.urls import path
from .views import DetailDataView
from . import views

app_name = "faktur"

urlpatterns = [
    path('browse/', views.items, name='items'),
    path('detail/<int:pk>/', DetailDataView.as_view(), name='detail'),
]
