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


def faktur2022(request, ID_PEMBELI):
    faktur = Faktur2022.objects.get(pk=ID_PEMBELI)
    context = {
        "faktur":faktur,
        }
    return render(request, "faktur/index.html", context)

def index(request):
    latest_faktur = Faktur2022.objects.order_by("-TGL_FAKTUR")[:5]
    # output = ", ".join([q.NAMA_PEMBELI for q in latest_faktur])
    context = {
        "latest_faktur": latest_faktur,
        }
    return render(request, "faktur/index.html", context)

