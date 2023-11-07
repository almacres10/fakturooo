from django.shortcuts import render
from faktur.models import Faktur2022
from django.views.generic.detail import DetailView

# Create your views here.
def index(request):
    latest_faktur = Faktur2022.objects.order_by("-TGL_FAKTUR")[:20]
    # output = ", ".join([q.NAMA_PEMBELI for q in latest_faktur])
    context = {
        "latest_faktur": latest_faktur,
        }
    return render(request, "core/index.html", context)