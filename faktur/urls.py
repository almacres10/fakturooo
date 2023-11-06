from django.urls import path
from .views import DetailDataView
from . import views

app_name = "faktur"

urlpatterns = [
    path("", views.index, name="index"),
    path('detail/<int:pk>/', DetailDataView.as_view(), name='detail'),
]
