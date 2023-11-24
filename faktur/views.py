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

def itemsFaktur(request, nama_pembeli):
    # Mendapatkan semua objek yang sesuai dengan kriteria pencarian
    data_pembeli_list = Faktur2022.objects.filter(NAMA_PEMBELI=nama_pembeli)

    # Menyusun data untuk dilewatkan ke template
    context = {
        'data_pembeli_list': data_pembeli_list,
    }

    return render(request, 'faktur/detail.html', context)

# def itemsFaktur(request):
#     nama_pembeli_data = request.GET.get('nama_pembeli', '')

#     if nama_pembeli_data:
#         data_pembeli_list = Faktur2022.objects.filter(NAMA_PEMBELI=nama_pembeli_data)
#         print(data_pembeli_list)  # Tambahkan ini untuk debug

#         context = {'data_pembeli_list': data_pembeli_list}
#         return render(request, 'faktur/detail.html', context)
#     else:
#         return render(request, 'faktur/missing_parameter.html')

