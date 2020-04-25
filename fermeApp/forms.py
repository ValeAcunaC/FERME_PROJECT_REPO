from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Usuario

class CreateUserForm(UserCreationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete':'new-password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','password1','password2']

class UsuarioForm(ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    rut = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'rut', 'telefono', 'direccion']
