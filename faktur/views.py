from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from . models import RekapFaktur000, Faktur2022
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
from django.http import Http404



# Create your views here.
class DetailDataView(DetailView):
    model = RekapFaktur000
    template_name = 'faktur/detail.html'
    context_object_name = 'data'

def resetItems(request):
    return render(request, 'faktur/items.html')

def items(request):
    query = request.GET.get('query', '')
    items = RekapFaktur000.objects.all()

    if query:
        items = items.filter(Q(nama_pembeli__icontains=query))

    items_per_page = 20
    paginator = Paginator(items, items_per_page)
    
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'faktur/items.html', {
        "page_obj": page_obj
    })

def itemsFaktur(request, id_pembeli):
    rekap_faktur = get_object_or_404(RekapFaktur000, id_pembeli=id_pembeli)
    nama_pembeli = rekap_faktur.nama_pembeli

    # Lakukan pencarian di model Faktur2022 berdasarkan nama_pembeli
    faktur_entries = Faktur2022.objects.filter(NAMA_PEMBELI=nama_pembeli)
    # print(str(faktur_entries.query))

    data_pembeli_list = [
        {
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

    # Menyusun data untuk dilewatkan ke template
    context = {
        'data_pembeli_list': data_pembeli_list,
    }

    return render(request, 'faktur/detail.html', context)
    
def download_csv(request, id_pembeli):
    # Dapatkan objek RekapFaktur000 berdasarkan id_pembeli
    rekap_faktur = get_object_or_404(RekapFaktur000, id_pembeli=id_pembeli)

    # Dapatkan nilai nama_pembeli dari objek RekapFaktur000
    nama_pembeli = rekap_faktur.nama_pembeli

    # Lakukan pencarian di model Faktur2022 berdasarkan nama_pembeli
    faktur_entries = Faktur2022.objects.filter(NAMA_PEMBELI=nama_pembeli)

    # Buat response untuk file CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{nama_pembeli}_faktur.csv"'

    # Buat objek CSV writer
    csv_writer = csv.writer(response)

    # Tulis header
    csv_writer.writerow(['ID_PEMBELI', 'KD_JNS_TRX', 'NO_FAKTUR', 'TGL_APPROVAL', '...'])

    # Tulis data
    for entry in faktur_entries:
        csv_writer.writerow([entry.ID_PEMBELI, entry.KD_JNS_TRX, entry.NO_FAKTUR, entry.TGL_APPROVAL, '...'])

    return response

