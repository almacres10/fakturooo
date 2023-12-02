from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from . models import RekapFaktur000, Faktur2022, RefWilayah
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
from django.http import Http404, JsonResponse
from . forms import PilihWilayah, PilihWilayahKecamatan
import time
from django.contrib.auth.decorators import login_required
from django.db.models import Count



# Awalnya Class yang dipakai untuk menampilkan banyak data ke satu context
# Tapi tidak jadi digunakan :)
@login_required(login_url='core:login')
class CombinedView(TemplateView):
    template_name = 'faktur/per_wilayah.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # # Mengambil seluruh data RekapFaktur000
        # data_list = RekapFaktur000.objects.all()

        # # Menggunakan Paginator untuk mempaginate data_list
        # paginator = Paginator(data_list, 20)  # Menentukan jumlah data per halaman
        # page = self.request.GET.get('page')  # Mendapatkan nomor halaman dari parameter URL

        # try:
        #     data_list_paginated = paginator.page(page)
        # except PageNotAnInteger:
        #     # Jika nomor halaman bukan integer, kembalikan halaman pertama
        #     data_list_paginated = paginator.page(1)
        # except EmptyPage:
        #     # Jika nomor halaman di luar rentang, kembalikan halaman terakhir
        #     data_list_paginated = paginator.page(paginator.num_pages)

        # context['data'] = data_list_paginated

        kelurahan_list = RefWilayah.objects.filter(KOTA='KOTA PAYAKUMBUH', KELURAHAN__isnull=False).values_list('KELURAHAN', flat=True).distinct()
        context['kelurahan_list'] = kelurahan_list

        kota_list = RefWilayah.objects.values_list('KOTA', flat=True).distinct()
        kota_list = [wilayah.replace('KAB. ', '').replace('KOTA ', '') for wilayah in kota_list]
        context['kota_list'] = kota_list

        kecamatan_list = RefWilayah.objects.values_list('KECAMATAN', 'KOTA').distinct()
        context['kecamatan_list'] = kecamatan_list

        kelurahan_list = RefWilayah.objects.values_list('KELURAHAN', 'KECAMATAN').distinct()
        context['kelurahan_list'] = kelurahan_list

        return context
    

# Fungsi untuk opening pencarian by nama
# Awalnya untuk menampilkan 20 Data Faktur Pajak dari Model Faktur2022
# Tapi tidak jadi dipakai, hanya untuk jembatan ke cari_faktur_nama.html
# Di html tersebut context tidak digunakan
def cariFakturNama(request):
    latest_faktur = Faktur2022.objects.all()[:20]
    # output = ", ".join([q.NAMA_PEMBELI for q in latest_faktur])
    context = {
        "latest_faktur": latest_faktur,
        }
    return render(request, "faktur/cari_faktur_nama.html", context)

# Fungsi untuk opening pencarian by alamat
# Awalnya untuk menampilkan 20 Data Faktur Pajak dari Model Faktur2022
# Tapi tidak jadi dipakai, hanya untuk jembatan ke cari_faktur_nama.html
# Di html tersebut context tidak digunakan
def cariFakturAlamat(request):
    latest_faktur = Faktur2022.objects.all()[:20]
    # output = ", ".join([q.NAMA_PEMBELI for q in latest_faktur])
    context = {
        "latest_faktur": latest_faktur,
        }
    return render(request, "faktur/cari_faktur_alamat.html", context)

# Fungsi untuk opening pencarian by alamat
# Awalnya untuk menampilkan 20 Data Faktur Pajak dari Model Faktur2022
# Tapi tidak jadi dipakai, hanya untuk jembatan ke cari_faktur_nama.html
# Di html tersebut context tidak digunakan
def cariFakturDetail(request):
    latest_faktur = Faktur2022.objects.all()[:20]
    # output = ", ".join([q.NAMA_PEMBELI for q in latest_faktur])
    context = {
        "latest_faktur": latest_faktur,
        }
    return render(request, "faktur/cari_faktur_detail.html", context)


# Fungsi untuk reset pencarian
# Masih dalam tahap penyempurnaan
@login_required(login_url='core:login')
def resetItems(request):
    return render(request, 'faktur/items.html')


# Fungsi buat cari Item by Nama
@login_required(login_url='core:login')
def items(request):
    query = request.GET.get('query', '')
    items = RekapFaktur000.objects.all()

    if query:
        items = items.filter(Q(nama_pembeli__icontains=query))

    # Khusus Paginator, rencana mau dibikin lagi fungsi khusus paginator ini
    items_per_page = 20
    paginator = Paginator(items, items_per_page)   
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'faktur/items_by_nama.html', {
        "page_obj": page_obj
    })

# Fungsi buat cari Item by Alamat
@login_required(login_url='core:login')
def items2(request):
    query = request.GET.get('query', '')
    items = RekapFaktur000.objects.all()

    if query:
        items = items.filter(Q(alamat_pembeli__icontains=query))

    items_per_page = 20
    paginator = Paginator(items, items_per_page)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'faktur/items_by_alamat.html', {
        "page_obj": page_obj
    })
    
# Fungsi buat cari Item by Detail
@login_required(login_url='core:login')
def items3(request):
    query = request.GET.get('query', '')
    
    # Lakukan operasi group by pada NAMA_BARANG dan hitung jumlah setiap grup
    grouped_items = Faktur2022.objects.values('NAMA_BARANG', 'NAMA_PEMBELI', 'ID_PEMBELI').annotate(count=Count('NAMA_BARANG'))

    if query:
        # Filter data yang memiliki NAMA_BARANG sesuai dengan query
        grouped_items = grouped_items.filter(Q(NAMA_BARANG__icontains=query))

    items_per_page = 20
    paginator = Paginator(grouped_items, items_per_page)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'faktur/items_by_faktur.html', {
        "page_obj": page_obj
    })

# Lanjutan Fungsi buat cari Item by Detail
@login_required(login_url='core:login')
def items3Next(request, id_pembeli):
    rekap_faktur = get_object_or_404(RekapFaktur000, id_pembeli=id_pembeli)
    nama_pembeli = rekap_faktur.nama_pembeli


    items_per_page = 20
    paginator = Paginator(rekap_faktur, items_per_page)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'faktur/items_by_nama.html', {
        "page_obj": page_obj
    })

# Fungsi untuk mendapatkan detail faktur, dengan mencocokkan id_pembeli dari parameter ke RekapFaktur000
# Kemudian ambil nama_pembeli yang sama dari Faktur2022 berdasarkan kecocokan di RekapFaktur000
def itemsFaktur(request, id_pembeli):
    try:
        # Mencoba untuk mendapatkan objek dari model RekapFaktur000
        rekap_faktur = get_object_or_404(RekapFaktur000, id_pembeli=id_pembeli)
    except RekapFaktur000.DoesNotExist:
        try:
            # Jika objek dari model RekapFaktur000 tidak ditemukan,
            # mencoba untuk mendapatkan objek dari model Faktur2022
            rekap_faktur = get_object_or_404(Faktur2022, id_pembeli=id_pembeli)
        except Faktur2022.DoesNotExist:
            # Jika kedua model tidak memiliki objek dengan id_pembeli yang diberikan,
            # raise Http404 untuk menampilkan halaman 404
            raise Http404("No RekapFaktur000 or Faktur2022 matches the given query.")

    # Jika kita mencapai titik ini, kita telah berhasil mendapatkan objek
    nama_pembeli = rekap_faktur.nama_pembeli

    # Fungsi get_data_pembeli_list ini ada dibawah
    data_pembeli_list = get_data_pembeli_list(nama_pembeli)

    # Menyusun data untuk dilewatkan ke template
    context = {
        'data_pembeli_list': data_pembeli_list,
    }

    return render(request, 'faktur/detail.html', context)


# Fungsi untuk melakukan filter data nama_pembeli di Faktur2022
def get_data_pembeli_list(nama_pembeli):
    faktur_entries = Faktur2022.objects.filter(NAMA_PEMBELI=nama_pembeli)
    
    data_pembeli_list = [
        {
            'ID_PEMBELI' : entry.ID_PEMBELI,
            'NO_FAKTUR': entry.NO_FAKTUR,
            'NPWP_PENJUAL': entry.NPWP_PENJUAL,
            'NAMA_PENJUAL': entry.NAMA_PENJUAL,
            'ALAMAT_PENJUAL': entry.ALAMAT_PENJUAL,
            'NAMA_PEMBELI': entry.NAMA_PEMBELI,
            'ALAMAT_PEMBELI': entry.ALAMAT_PEMBELI,
            'NAMA_BARANG': entry.NAMA_BARANG,
            'JML_PPN': entry.JML_PPN,
            # ... tambahkan atribut lain sesuai kebutuhan
        }
        for entry in faktur_entries
    ]

    return data_pembeli_list



# Fungsi untuk memdowmload file CSV
@login_required(login_url='core:login')
def download_csv(request, id_pembeli):
    rekap_faktur = get_object_or_404(Faktur2022, ID_PEMBELI=id_pembeli)
    nama_pembeli = rekap_faktur.NAMA_PEMBELI

    # Menggunakan data_pembeli_list dari fungsi utilitas
    data_pembeli_list = get_data_pembeli_list(nama_pembeli)

    # Membuat nama file CSV berdasarkan variabel nama_pembeli
    csv_filename = f"data_pembeli_list_{nama_pembeli}.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{csv_filename}"'

    # Tulis data ke response sebagai file CSV
    writer = csv.writer(response)
    # Tulis header
    writer.writerow(data_pembeli_list[0].keys())
    # Tulis data
    for entry in data_pembeli_list:
        writer.writerow(entry.values())

    return response

# Fungsi untuk menampilkan form pilih wilayah kabupateb/kota yang mau dicari
@login_required(login_url='core:login')
def form_wilayah(request):
    form = PilihWilayah()
    return render(request, 'faktur/per_wilayah.html', {'form': form})

# Fungsi untuk mencari berdasarkan wilayah yang dipilih
@login_required(login_url='core:login')
def get_wilayah(request):
    form = PilihWilayah(request.GET)

    if form.is_valid():
        selected_wilayah = form.cleaned_data['wilayah_field']
        items = RekapFaktur000.objects.all()
        items = items.filter(Q(alamat_pembeli__icontains=selected_wilayah))

        items_per_page = 20
        paginator = Paginator(items, items_per_page)
        
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Include the form data and the current page number in the context
        context = {
            "data": page_obj,
            "form": form,
            "form_data": form.cleaned_data,  # Use cleaned_data instead of request.GET.urlencode()
            "current_page_number": page_obj.number,
        }

        return render(request, 'faktur/hasil_cari_per_wilayah.html', context)
    return render(request, 'faktur/hasil_cari_per_wilayah.html', {'form': form})

# Fungsi yang tidak jadi dipakai, karena hanya mendownload berdasarkan ada faktur yang mengandung
# kata kota/kabupaten yang dipilih
@login_required(login_url='core:login')
def download_all_csv(request):
    # Catat waktu awal eksekusi view
    start_time = time.time()

    form = PilihWilayah(request.GET)

    if form.is_valid():
        selected_wilayah = form.cleaned_data['wilayah_field']
        items = Faktur2022.objects.all()
        items = items.filter(ALAMAT_PEMBELI__icontains=selected_wilayah)

        # Create response with CSV content
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="wilayah_{selected_wilayah}_report.csv"'

        # Create CSV writer
        csv_writer = csv.writer(response)

        # Write header
        csv_writer.writerow(['ID_PEMBELI', 'KD_JNS_TRX', 'ID_STS_PENGGANTI', 'NO_FAKTUR', 'TGL_APPROVAL', 'TGL_FAKTUR', 'ID_STS_FAKTUR',
                             'FG_UANG_MUKA', 'ID_MS_TH_PJK', 'NPWP_PENJUAL', 'NAMA_PENJUAL', 'ALAMAT_PENJUAL', 'ID_JNS_WP_PENJUAL', 'KPPADM_PENJUAL',
                             'KD_KLU_PENJUAL', 'NPWP_PEMBELI', 'NAMA_PEMBELI', 'ALAMAT_PEMBELI', 'ID_JNS_WP_PEMBELI', 'KPPADM_PEMBELI', 'KD_KLU_PEMBELI',
                             'ID_FP_PENGGANTI', 'JML_BARANG', 'NAMA_BARANG', 'HARGA_SATUAN', 'HARGA_TOTAL', 'DISKON', 'JML_DPP',
                             'JML_PPN', 'JML_PPNBM', 'TARIF_PPNBM', 'KODE_OBJEK',])


        # Write data
        for item in items:
            csv_writer.writerow([item.ID_PEMBELI, item.KD_JNS_TRX, item.ID_STS_PENGGANTI, item.NO_FAKTUR,
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

    # Handle invalid form
    return render(request, 'faktur/hasil_cari_per_wilayah.html', {'form': form})

# Fungsi yang dipakai, karena mendownload berdasarkan ada faktur yang mengandung
# kata kecamatan berdasarkan kota/kabupaten yang dipilih
@login_required(login_url='core:login')
def download_all_csv_kecamatan(request):
    # Catat waktu awal eksekusi view
    start_time = time.time()

    form = PilihWilayah(request.GET)
    if form.is_valid():
        selected_kota = form.cleaned_data['wilayah_field']
        query_kelurahan = RefWilayah.objects.filter(KOTA=selected_kota, KELURAHAN__isnull=False).values_list('KELURAHAN', flat=True).distinct()
        query_kelurahan_list = list(query_kelurahan)
        query_kecamatan = RefWilayah.objects.filter(KOTA=selected_kota, KECAMATAN__isnull=False).values_list('KECAMATAN', flat=True).distinct()
        query_kecamatan_list = list(query_kecamatan)
        query_kota = RefWilayah.objects.filter(KOTA=selected_kota)
        query_kota_list = list(query_kota)
        combined_list = query_kelurahan_list + query_kecamatan_list + query_kota_list

        # Menggabungkan ketiga query menjadi satu
        items = []
        for kata in query_kecamatan_list:
             items.extend(Faktur2022.objects.filter(ALAMAT_PEMBELI__icontains=kata))

        # Create response with CSV content
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="wilayah_report.csv"'

        # Create CSV writer
        csv_writer = csv.writer(response)
        
        csv_writer.writerow(['ID_PEMBELI', 'KD_JNS_TRX', 'ID_STS_PENGGANTI', 'NO_FAKTUR', 'TGL_APPROVAL', 'TGL_FAKTUR', 'ID_STS_FAKTUR',
                             'FG_UANG_MUKA', 'ID_MS_TH_PJK', 'NPWP_PENJUAL', 'NAMA_PENJUAL', 'ALAMAT_PENJUAL', 'ID_JNS_WP_PENJUAL', 'KPPADM_PENJUAL',
                             'KD_KLU_PENJUAL', 'NPWP_PEMBELI', 'NAMA_PEMBELI', 'ALAMAT_PEMBELI', 'ID_JNS_WP_PEMBELI', 'KPPADM_PEMBELI', 'KD_KLU_PEMBELI',
                             'ID_FP_PENGGANTI', 'JML_BARANG', 'NAMA_BARANG', 'HARGA_SATUAN', 'HARGA_TOTAL', 'DISKON', 'JML_DPP',
                             'JML_PPN', 'JML_PPNBM', 'TARIF_PPNBM', 'KODE_OBJEK',])


        # Write data
        for item in items:
            csv_writer.writerow([item.ID_PEMBELI, item.KD_JNS_TRX, item.ID_STS_PENGGANTI, item.NO_FAKTUR,
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

    return render(request, 'faktur/hasil_cari_per_wilayah.html', {'form': form})
