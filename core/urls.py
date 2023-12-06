from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from . forms import LoginForm


app_name = 'core'

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    # path('', views.index, name='index'),
    # path('contact/', views.contact, name='contact'),
    # path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.index, name='index'),
    path('perkpp', views.get_wilayah, name='cari_per_kpp'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register, name='register'),
    path('chartjs/', views.chart_view, name='chartjs-view'),
    path('summary/', views.summary_view, name='summary_view'),
    path('download_wilayah_csv_kpp/', views.download_all_csv_kecamatan, name='download_all_csv_kecamatan')
]