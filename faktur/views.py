from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from . models import RekapFaktur000, Faktur2022, RefWilayah
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
from django.http import Http404



# Create your views here.
# class DataListView(ListView):
#     model = RekapFaktur000
#     template_name = 'faktur/per_wilayah.html'
#     context_object_name = 'data'
#     paginate_by = 20  # Menentukan jumlah data per halaman

#     def get_queryset(self):
#         # Mengambil seluruh data RekapFaktur000
#         return RekapFaktur000.objects.all()


class CombinedView(TemplateView):
    template_name = 'faktur/per_wilayah.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Mengambil seluruh data RekapFaktur000
        data_list = RekapFaktur000.objects.all()

        # Menggunakan Paginator untuk mempaginate data_list
        paginator = Paginator(data_list, 20)  # Menentukan jumlah data per halaman
        page = self.request.GET.get('page')  # Mendapatkan nomor halaman dari parameter URL

        try:
            data_list_paginated = paginator.page(page)
        except PageNotAnInteger:
            # Jika nomor halaman bukan integer, kembalikan halaman pertama
            data_list_paginated = paginator.page(1)
        except EmptyPage:
            # Jika nomor halaman di luar rentang, kembalikan halaman terakhir
            data_list_paginated = paginator.page(paginator.num_pages)

        context['data'] = data_list_paginated

        # Mengambil data wilayah dari list
        wilayah_list = [
            "KAB. PESISIR SELATAN", "KAB. TANAH DATAR", "KAB. SOLOK", "KAB. SIJUNJUNG",
            "KAB. PADANG PARIAMAN", "KAB. AGAM", "KAB. LIMA PULUH KOTA", "KAB. PASAMAN",
            "KAB. KEPULAUAN MENTAWAI", "KAB. PASAMAN BARAT", "KAB. SOLOK SELATAN", "KAB. DHARMASRAYA",
            "KOTA PADANG", "KOTA PADANG PANJANG", "KOTA BUKITTINGGI", "KOTA PAYAKUMBUH", "KOTA SOLOK",
            "KOTA PARIAMAN", "KOTA SAWAHLUNTO", "KAB. KERINCI", "KAB. MERANGIN", "KAB. SAROLANGUN",
            "KAB. BATANGHARI", "KAB. MUARO JAMBI", "KAB. TANJUNG JABUNG TIMUR", "KAB. TANJUNG JABUNG BARAT",
            "KAB. BUNGO", "KOTA SUNGAI PENUH", "KOTA JAMBI", "KAB. TEBO"
        ]
        context['wilayah_list'] = wilayah_list

        return context

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

    data_pembeli_list = get_data_pembeli_list(nama_pembeli)

    # Menyusun data untuk dilewatkan ke template
    context = {
        'data_pembeli_list': data_pembeli_list,
    }

    return render(request, 'faktur/detail.html', context)   

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

def showWilayah(request):
    wilayah_list = RefWilayah.objects.all()
    return render(request, 'faktur/per_wilayah.html', {'wilayah_list': wilayah_list})