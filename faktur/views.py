from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from . models import Faktur2022
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv



# Create your views here.
class DetailDataView(DetailView):
    model = Faktur2022
    template_name = 'faktur/detail.html'
    context_object_name = 'data'

# def items(request):
#     query = request.GET.get('query', '')
#     items = Faktur2022.objects.all()

#     if query:
#         items = items.filter(Q(NAMA_PEMBELI__icontains=query))

#     items_per_page = 10
#     paginator = Paginator(items, items_per_page)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'faktur/items.html', {
#         "page_obj":page_obj
#     })

def items(request):
    query = request.GET.get('query', '')
    items = Faktur2022.objects.all()

    if query:
        items = items.filter(Q(NAMA_PEMBELI__icontains=query))[:20]

    items_per_page = 10
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

def download_items(request):
    query = request.GET.get('query', '')
    items = Faktur2022.objects.all()

    if query:
        items = items.filter(Q(NAMA_PEMBELI__icontains=query))

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="items.csv"'

    # Create a CSV writer and write the header
    writer = csv.writer(response)
    writer.writerow(['ID_PEMBELI','NO_FAKTUR','TGL_FAKTUR','ID_MS_TH_PJK','NPWP_PENJUAL','NAMA_PENJUAL',
                     'ALAMAT_PENJUAL','NPWP_PEMBELI','NAMA_PEMBELI','ALAMAT_PEMBELI','JML_BARANG','NAMA_BARANG',
                     'JML_DPP','JML_PPN'])

    # Write data to the CSV file
    for item in items:
        writer.writerow([item.ID_PEMBELI,item.NO_FAKTUR,item.TGL_FAKTUR,item.ID_MS_TH_PJK,item.NPWP_PENJUAL,item.NAMA_PENJUAL,
                         item.ALAMAT_PENJUAL,item.NPWP_PEMBELI,item.NAMA_PEMBELI,item.ALAMAT_PEMBELI,item.JML_BARANG,item.NAMA_BARANG,
                         item.JML_DPP,item.JML_PPN]) 
    return response
