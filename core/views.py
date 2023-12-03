from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from faktur.models import Faktur2022
from django.views.generic.detail import DetailView
from . forms import SignupForm, PilihKPP
from faktur.models import RekapFaktur000, RefWilayah
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




# Create your views here.
def index(request):
    latest_faktur = Faktur2022.objects.all()[:20]
    # output = ", ".join([q.NAMA_PEMBELI for q in latest_faktur])
    context = {
        "latest_faktur": latest_faktur,
        }
    return render(request, "core/index.html", context)

def summary_view(request):
    # # Mengambil data RekapFaktur000 dan mengurutkannya berdasarkan nil_ppn secara descending
    # summary_data = RekapFaktur000.objects.order_by('-nil_ppn')[:15]  # Ambil 10 data teratas

    # # Menyusun data untuk dilewatkan ke template
    # context = {
    #     'summary_data': summary_data,
    # }

    form = PilihKPP()
    context = {
        'form': form,
    }

    return render(request, 'core/summary.html', context)

def get_wilayah(request):
    form = PilihKPP(request.GET)
    
    if form.is_valid():
        selected_kppadm = form.cleaned_data['wilayah_field']
        kpp_by_kppadm = RefWilayah.objects.filter(KPPADM=selected_kppadm)
        kecamatan_by_kppadm = kpp_by_kppadm.values_list('KECAMATAN', flat=True)

        print("Kecamatan_by_kppadm:")
        for kecamatan in kecamatan_by_kppadm:
            print(kecamatan)

        items = RekapFaktur000.objects.all()
        items = items.filter(alamat_pembeli__in=kecamatan_by_kppadm)

        items_per_page = 20
        paginator = Paginator(items, items_per_page)
        
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            "data": page_obj,
            "form": form,
            "form_data": form.cleaned_data,  # Use cleaned_data instead of request.GET.urlencode()
            "current_page_number": page_obj.number,
        }

        return render(request, 'core/hasil_cari_per_wilayah.html', context)
    return render(request, 'core/hasil_cari_per_wilayah.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('core:login')

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

def chart_view(request):
    # Mendapatkan data dari model atau sumber data lainnya
    data = [10, 20, 30, 40, 50]

    # Menyediakan data ke template dalam bentuk JSON
    context = {'data': json.dumps(data)}

    return render(request, 'core/chart_js.html', context)