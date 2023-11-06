from django.urls import path

from . import views

app_name = "faktur"

urlpatterns = [
    path("<int:id>/", views.faktur2022, name="faktur")
]
