from django.shortcuts import render, get_object_or_404
from . models import Faktur2022

# Create your views here.
def faktur2022(request, id):
    faktur = Faktur2022.objects.get(pk=id)
    context = {
        "faktur":faktur,
        }
    return render(request, "faktur/index.html", context)