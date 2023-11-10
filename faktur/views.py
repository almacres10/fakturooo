from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from . models import Faktur2022
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




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
        items = items.filter(Q(NAMA_PEMBELI__icontains=query))

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
