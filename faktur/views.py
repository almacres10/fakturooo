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

