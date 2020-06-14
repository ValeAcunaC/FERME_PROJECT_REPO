import django_filters
from django_filters import DateFilter, CharFilter
from django import forms
from django.db.models.query import QuerySet

from .models import *
#existe exclude! ej: exclude = ['id','nombre']
#start_date = DateFilter(field_name="date_created", lookup_expr='gte')
#gte -> greater than or equeal. lte -> lower than or equal
class CategoriaFilter(django_filters.FilterSet):
    nombrecategoria = CharFilter(label='Nombre Categoria' ,field_name='nombrecategoria', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Categoria
        fields = ['nombrecategoria']

class SubcategoriaFilter(django_filters.FilterSet):
    nombresubcategoria = CharFilter(label='Nombre Subcategoria' ,field_name='nombresubcategoria', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    idcategoria = django_filters.ModelChoiceFilter(queryset=Categoria.objects.all(), label='Categoria' ,field_name='idcategoria', widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Subcategoria
        fields = '__all__'

class ProductoFilter(django_filters.FilterSet):
    idproducto = CharFilter(label='Codigo' ,field_name='idproducto', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    nombreproducto = CharFilter(label='Nombre producto' ,field_name='nombreproducto', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    marca = CharFilter(label='Marca' ,field_name='marca', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    precio = CharFilter(label='Precio' ,field_name='precio', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    fechavencimiento = CharFilter(label='Fecha de Vencimiento' ,field_name='fechavencimiento', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    #stock = CharFilter(label='Stock' ,field_name='stock', widget=django_filters.widgets.RangeWidget(attrs={'class':'form-control'}))
    idsubcategoria = django_filters.ModelChoiceFilter(queryset=Subcategoria.objects.all(), label='Subcategoria' ,field_name='idsubcategoria', widget=forms.Select(attrs={'class':'form-control'}))
    idproveedor = django_filters.ModelChoiceFilter(queryset=Proveedor.objects.all(), label='Proveedor' ,field_name='idproveedor', widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Producto
        fields = '__all__'
        exclude = ['descripcion','stock','stockcritico','foto']

class ProveedorFilter(django_filters.FilterSet):
    nombreproveedor = CharFilter(label='Nombre proveedor' ,field_name='nombreproveedor', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    rutproveedor = CharFilter(label='Rut proveedor' ,field_name='rutproveedor', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    correo = CharFilter(label='Correo proveedor' ,field_name='correo', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    telefono = CharFilter(label='Telefono' ,field_name='telefono', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    idrubro = django_filters.ModelChoiceFilter(queryset=Rubro.objects.all(), label='Rubro' ,field_name='idrubro', widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Proveedor
        fields = '__all__'

class UserFilter(django_filters.FilterSet):
    username = CharFilter(label='Correo' ,field_name='username', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = CharFilter(label='Nombre' ,field_name='first_name', lookup_expr='icontains', widget=forms.TextInput(attrs={'class':'form-control'}))
    #username = CharFilter(label='Correo' ,field_name='username', lookup_expr='icontains')
    #first_name = CharFilter(label='Nombre' ,field_name='first_name', lookup_expr='icontains')
    #last_name = CharFilter(label='Apellido' ,field_name='last_name', lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['username', 'first_name']
        #fields = ['username', 'first_name', 'last_name']#usamos solo nombre en el display, quizas podemos cambiar a ambos por separado o concatenados
        #fields = '__all__'
        #exclude = ['password','is_superuser','is_staff','email', 'groups']
