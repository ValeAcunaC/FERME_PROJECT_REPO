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
    fechavencimiento = forms.DateField(required=False, widget=forms.DateInput(attrs={'class':'form-control'}))
    idsubcategoria = forms.ModelChoiceField(queryset=Subcategoria.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    idproveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))
    foto = forms.ImageField(required = False)
    
    class Meta:
        model = Producto
        fields = ['idproducto', 'nombreproducto', 'descripcion', 'stock', 'stockcritico', 'precio', 'marca', 'fechavencimiento', 'idsubcategoria', 'idproveedor','foto']

class ModificarProductoForm(ModelForm):
    
    nombreproducto = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    stock = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    stockcritico = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    precio = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    marca = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    foto = forms.ImageField(required = False)
    
    class Meta:
        model = Producto
        fields = ['nombreproducto', 'descripcion', 'stock', 'stockcritico', 'precio', 'marca','foto']

class StaffForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #username = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    #password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    is_staff = forms.IntegerField(widget=forms.HiddenInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name','last_name', 'is_staff']

class OrdencompraForm(ModelForm):
    #def __init__(self,usuario,estadocreado,*args,**kwargs):
        #super(OrdencompraForm,self).__init__(*args,**kwargs)
        #self.fields['idusuario']= forms.ModelChoiceField(label='Usuario', disabled = True , initial=1 , queryset=Usuario.objects.filter(id=usuario),widget=forms.Select(attrs={'class':'form-control'}))
        #self.fields['idestadooc']= forms.ModelChoiceField(label='Estadoordencompra', disabled = True , initial=1 , queryset=Estadoordencompra.objects.filter(idestadooc=estadocreado),widget=forms.Select(attrs={'class':'form-control'}))
    
    idusuario = forms.ModelChoiceField(label='Usuario', queryset=Usuario.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))
    idestadooc = forms.ModelChoiceField(label='Estadoordencompra', disabled = True , initial=1 , queryset=Estadoordencompra.objects.filter(nombreestadooc__contains="Creado"),widget=forms.Select(attrs={'class':'form-control'}))
    #idusuario = forms.IntegerField(widget=forms.HiddenInput(attrs={'class':'form-control'}))
    #idestadooc = forms.CharField(label='Estado', widget=forms.HiddenInput(attrs={'class':'form-control'}))
    idproveedor = forms.ModelChoiceField(label='Proveedor', queryset=Proveedor.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))
    comentarios = forms.CharField(label='Comentarios', required = False, widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Ordencompra
        fields = ['idusuario','idestadooc','idproveedor','comentarios']

class OrdencompraproductoForm(ModelForm):
    #idordencompra = forms.CharField(widget=forms.HiddenInput(attrs={'class':'form-control'}))
    #idproducto = forms.ModelChoiceField(label='Producto', queryset=Producto.objects.all(), widget=forms.Select(attrs={'class':'form-control-sm'}))
    #idcantidadoc = forms.CharField(label='Cantidad', widget=forms.TextInput(attrs={'class':'form-control-sm'}))
    class Meta:
        model = OrdencompraProducto
        fields = ['idordencompra','idproducto','cantidadoc']       



