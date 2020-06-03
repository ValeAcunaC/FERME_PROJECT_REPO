import django_filters
from django_filters import DateFilter, CharFilter

from .models import *
#existe exclude! ej: exclude = ['id','nombre']
#start_date = DateFilter(field_name="date_created", lookup_expr='gte')
#gte -> greater than or equeal. lte -> lower than or equal
class CategoriaFilter(django_filters.FilterSet):
    nombrecategoria = CharFilter(label='Nombre Categoria' ,field_name='nombrecategoria', lookup_expr='icontains')
    class Meta:
        model = Categoria
        fields = ['nombrecategoria']

class SubcategoriaFilter(django_filters.FilterSet):
    nombresubcategoria = CharFilter(label='Nombre Subcategoria' ,field_name='nombresubcategoria', lookup_expr='icontains')
    class Meta:
        model = Subcategoria
        fields = '__all__'

class ProductoFilter(django_filters.FilterSet):
    nombreproducto = CharFilter(label='Nombre producto' ,field_name='nombreproducto', lookup_expr='icontains')
    class Meta:
        model = Producto
        fields = '__all__'
        exclude = ['descripcion','stock','stockcritico']

class ProveedorFilter(django_filters.FilterSet):
    nombreproveedor = CharFilter(label='Nombre proveedor' ,field_name='nombreproveedor', lookup_expr='icontains')
    rutproveedor = CharFilter(label='Rut proveedor' ,field_name='rutproveedor', lookup_expr='icontains')
    correo = CharFilter(label='Correo proveedor' ,field_name='correo', lookup_expr='icontains')
    class Meta:
        model = Proveedor
        fields = '__all__'

class UserFilter(django_filters.FilterSet):
    username = CharFilter(label='Correo' ,field_name='username', lookup_expr='icontains')
    first_name = CharFilter(label='Nombre' ,field_name='first_name', lookup_expr='icontains')
    #last_name = CharFilter(label='Apellido' ,field_name='last_name', lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['username', 'first_name']
        #fields = ['username', 'first_name', 'last_name']#usamos solo nombre en el display, quizas podemos cambiar a ambos por separado o concatenados
        #fields = '__all__'
        #exclude = ['password','is_superuser','is_staff','email', 'groups']
