from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
from django.db.models.query import QuerySet

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

class CategoriaForm(ModelForm):
    nombrecategoria = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Categoria
        fields = ['nombrecategoria']

class SubcategoriaForm(ModelForm):
    nombresubcategoria = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    idcategoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Subcategoria
        fields = ['nombresubcategoria', 'idcategoria']
    
class ProveedorForm(ModelForm):
    rutproveedor = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    nombreproveedor = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    telefono = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    correo = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    idrubro = forms.ModelChoiceField(queryset=Rubro.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Proveedor
        fields = ['rutproveedor', 'nombreproveedor', 'telefono', 'correo', 'idrubro']

class ProductoForm(ModelForm):
    idproducto = forms.CharField(widget=forms.HiddenInput(attrs={'class':'form-control'}))
    nombreproducto = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    stock = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    stockcritico = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    precio = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    marca = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    fechavencimiento = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control'}))
    idsubcategoria = forms.ModelChoiceField(queryset=Subcategoria.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    idproveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))
    
    class Meta:
        model = Producto
        fields = ['idproducto', 'nombreproducto', 'descripcion', 'stock', 'stockcritico', 'precio', 'marca', 'fechavencimiento', 'idsubcategoria', 'idproveedor']

class StaffForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #username = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    is_staff = forms.IntegerField(widget=forms.HiddenInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name','last_name', 'is_staff']



        



