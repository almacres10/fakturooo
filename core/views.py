from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from faktur.models import Faktur2022
from django.views.generic.detail import DetailView
from . forms import SignupForm, PilihKPP
from faktur.models import RekapFaktur000, RefWilayah
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
import csv
import time
from django.db.models import Count





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
        kecamatan_by_kppadm = kpp_by_kppadm.values_list('KECAMATAN', flat=True).distinct()

        # print("Kecamatan_by_kppadm:")
        # for kecamatan in kecamatan_by_kppadm:
        #     print(kecamatan)

        items = RekapFaktur000.objects.all()

        filter_query = Q()
        for kecamatan in kecamatan_by_kppadm:
            filter_query |= Q(alamat_pembeli__icontains=kecamatan)

         # Terapkan filter_query pada items
        items = items.filter(filter_query)
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

def download_all_csv_kecamatan(request):
    if request.method == 'GET':
        start_time = time.time()

        form_data = request.GET.dict()
        
        # Dapatkan data yang sesuai dengan form_data
        selected_kppadm = form_data.get('wilayah_field')
        kpp_by_kppadm = RefWilayah.objects.filter(KPPADM=selected_kppadm)
        kecamatan_by_kppadm = kpp_by_kppadm.values_list('KECAMATAN', flat=True).distinct()

        items = Faktur2022.objects.all()

        filter_query = Q()
        for kecamatan in kecamatan_by_kppadm:
            filter_query |= Q(ALAMAT_PEMBELI__icontains=kecamatan)

        items = items.filter(filter_query)

        # Buat file CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID_PEMBELI', 'KD_JNS_TRX', 'ID_STS_PENGGANTI', 'NO_FAKTUR', 'TGL_APPROVAL', 'TGL_FAKTUR', 'ID_STS_FAKTUR',
                             'FG_UANG_MUKA', 'ID_MS_TH_PJK', 'NPWP_PENJUAL', 'NAMA_PENJUAL', 'ALAMAT_PENJUAL', 'ID_JNS_WP_PENJUAL', 'KPPADM_PENJUAL',
                             'KD_KLU_PENJUAL', 'NPWP_PEMBELI', 'NAMA_PEMBELI', 'ALAMAT_PEMBELI', 'ID_JNS_WP_PEMBELI', 'KPPADM_PEMBELI', 'KD_KLU_PEMBELI',
                             'ID_FP_PENGGANTI', 'JML_BARANG', 'NAMA_BARANG', 'HARGA_SATUAN', 'HARGA_TOTAL', 'DISKON', 'JML_DPP',
                             'JML_PPN', 'JML_PPNBM', 'TARIF_PPNBM', 'KODE_OBJEK',])
        
        # Write data
        for item in items:
            writer.writerow([item.ID_PEMBELI, item.KD_JNS_TRX, item.ID_STS_PENGGANTI, item.NO_FAKTUR,
                                 item.TGL_APPROVAL, item.TGL_FAKTUR, item.ID_STS_FAKTUR, item.FG_UANG_MUKA,
                                 item.ID_MS_TH_PJK, item.NPWP_PENJUAL, item.NAMA_PENJUAL, item.ALAMAT_PENJUAL,
                                 item.ID_JNS_WP_PENJUAL, item.KPPADM_PENJUAL, item.KD_KLU_PENJUAL, item.NPWP_PEMBELI,
                                 item.NAMA_PEMBELI, item.ALAMAT_PEMBELI, item.ID_JNS_WP_PEMBELI, item.KPPADM_PEMBELI,
                                 item.KD_KLU_PEMBELI, item.ID_FP_PENGGANTI, item.JML_BARANG, item.NAMA_BARANG,
                                 item.HARGA_SATUAN, item.HARGA_TOTAL, item.DISKON, item.JML_DPP,
                                 item.JML_PPN, item.JML_PPNBM, item.TARIF_PPNBM, item.KODE_OBJEK,])
        # Catat waktu akhir eksekusi view
        end_time = time.time()

        # Hitung dan cetak waktu yang dibutuhkan
        processing_time = end_time - start_time
        print(f"Processing time: {processing_time} seconds")

        return response
    else:
        # Handle jika bukan request GET
        return HttpResponse("Method not allowed")

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