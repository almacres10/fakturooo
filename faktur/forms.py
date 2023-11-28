from django import forms
from .models import RefWilayah

# Ambil nilai KOTA dari database dan hilangkan awalan 'KAB.' dan 'KOTA'
wilayah_list = RefWilayah.objects.values_list('KOTA', flat=True).distinct()
wilayah_list = [(wilayah, wilayah.replace('KAB. ', '').replace('KOTA ', '')) for wilayah in wilayah_list]

class PilihWilayah(forms.Form):
    OPTIONS = wilayah_list

    wilayah_field = forms.ChoiceField(
        choices=OPTIONS,
        widget=forms.Select(attrs={'class': 'custom-select'}),
        label='Pilih salah satu opsi'
    )
