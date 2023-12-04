from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . models import User, Employee
from faktur.models import RefWilayah

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
        
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your Password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Name',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your Password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))


class PilihKPP(forms.Form):
    wilayah_field = forms.ChoiceField(
        choices=[('', 'Pilih KPP')] + list(RefWilayah.objects.values_list('KPPADM', 'KPPADM').distinct()),
        widget=forms.Select(attrs={'class': 'custom-select'}),
        label='Kode KPP'
    )

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': 'w-full py-4 px-6 mb-4 rounded-xl'
    }))

    nama_pegawai = forms.CharField(
        max_length=100,
        help_text='Required.',
        widget=forms.TextInput(attrs={'class': 'w-full py-4 px-6 mb-4 rounded-xl'}),
    )

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your Password',
        'class': 'w-full py-4 px-6 mb-4 rounded-xl'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'w-full py-4 px-6 mb-4 rounded-xl'
    }))