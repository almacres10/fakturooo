from django import forms
from .models import RefWilayah

# Ambil nilai KOTA dari database dan hilangkan awalan 'KAB.' dan 'KOTA'
wilayah_list = RefWilayah.objects.values_list('KOTA', flat=True).distinct()
wilayah_list =[('', 'Pilih Kabupaten/Kota')] + [(wilayah, wilayah.replace('KAB. ', '').replace('KOTA ', '').replace('KEPULAUAN ', '')) for wilayah in wilayah_list]

class PilihWilayah(forms.Form):
    OPTIONS = wilayah_list

    wilayah_field = forms.ChoiceField(
        choices=OPTIONS,
        widget=forms.Select(attrs={'class': 'custom-select'}),
        label='Pilih Kabupaten/Kota'
    )

# Ambil nilai KECAMATAN dari database dan hilangkan awalan 'KAB.' dan 'KOTA'
kecamatan_list = RefWilayah.objects.values_list('KECAMATAN', flat=True).distinct()

class PilihWilayahKecamatan(forms.Form):
    OPTIONS2 = kecamatan_list

    wilayah_kecamatan_field = forms.ChoiceField(
        choices= OPTIONS2,
        widget=forms.Select(attrs={'class': 'custom-select'}),
        label='Pilih salah satu opsi'
    )