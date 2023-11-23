from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from . models import RekapFaktur000, Faktur2022
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv



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

def itemsFaktur(request):
    # Dapatkan nilai 'nama_pembeli' dari parameter URL
    nama_pembeli = request.GET.get('nama_pembeli', '')
    
    # Gunakan nilai 'nama_pembeli' dalam filter queryset
    items = Faktur2022.objects.all()
    if nama_pembeli:
        items = items.filter(Q(nama_pembeli__icontains=nama_pembeli))

    items_per_page = 20
    paginator = Paginator(items, items_per_page)
    
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'faktur/detail.html', {
        "page_obj_detail": page_obj,
        "nama_pembeli": nama_pembeli  # Sertakan nilai nama_pembeli dalam konteks
    })