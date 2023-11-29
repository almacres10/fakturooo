from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from faktur.models import Faktur2022
from django.views.generic.detail import DetailView
from . forms import SignupForm
from . models import User


# Create your views here.
def index(request):
    latest_faktur = Faktur2022.objects.all()[:20]
    # output = ", ".join([q.NAMA_PEMBELI for q in latest_faktur])
    context = {
        "latest_faktur": latest_faktur,
        }
    return render(request, "core/index.html", context)

def user_logout(request):
    logout(request)
    return redirect('core:login')

# def download_all_csv(request):
#     form = PilihWilayah(request.GET)
#     if form.is_valid():
#         selected_kota = form.cleaned_data['wilayah_field']
#         query_kelurahan = RefWilayah.objects.filter(KOTA=selected_kota, KELURAHAN__isnull=False).values_list('KELURAHAN', flat=True).distinct()
#         query_kelurahan_list = list(query_kelurahan)
#         query_kecamatan = RefWilayah.objects.filter(KOTA=selected_kota, KECAMATAN__isnull=False).values_list('KECAMATAN', flat=True).distinct()
#         query_kecamatan_list = list(query_kecamatan)
#         query_kota = RefWilayah.objects.filter(KOTA=selected_kota)
#         query_kota_list = list(query_kota)
#         combined_list = query_kelurahan_list + query_kecamatan_list + query_kota_list

#         # Menggabungkan ketiga query menjadi satu
#         items = []
#         for kata in query_kecamatan_list:
#              items.extend(Faktur2022.objects.filter(ALAMAT_PEMBELI__icontains=kata))

#         # Create response with CSV content
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="wilayah_report.csv"'

#         # Create CSV writer
#         csv_writer = csv.writer(response)
        
#         # Write header
#         csv_writer.writerow(['Nama Pembeli', 'Alamat Pembeli'])

#         # Write data
#         for item in items:
#             csv_writer.writerow([item.nama_pembeli, item.alamat_pembeli])

#         return response

#     # Handle invalid form
#     return render(request, 'faktur/cari_per_wilayah.html', {'form': form})

def user_signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:login')
        else:
            form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})