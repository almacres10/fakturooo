from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404
from . models import Faktur2022
from django.db.models import Q
from django.http import HttpResponse



# Create your views here.
class DetailDataView(DetailView):
    model = Faktur2022
    template_name = 'faktur/detail.html'
    context_object_name = 'data'

def items(request):
    query = request.GET.get('query', '')
    items = Faktur2022.objects.all()

    if query:
        items = items.filter(Q(NAMA_PEMBELI__icontains=query))

    return render(request, 'faktur/items.html', {
        'query': query,
        'items': items, 
    })
