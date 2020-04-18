from django.contrib import admin

# Register your models here.
from . models import Usuario, Boleta, Categoria, Despacho, Estadodespacho, Estadoordencompra, Estadopago, Estadoventa, Factura, Ordencompra, OrdencompraProducto, Pago, Producto, Proveedor, Rubro, Subcategoria, Tipopago, Venta, VentaProducto

admin.site.register(Usuario)
admin.site.register(Boleta)
admin.site.register(Categoria)
admin.site.register(Despacho)
admin.site.register(Estadodespacho)
admin.site.register(Estadoordencompra)
admin.site.register(Estadopago)
admin.site.register(Estadoventa)
admin.site.register(Factura)
admin.site.register(Ordencompra)
admin.site.register(OrdencompraProducto)
admin.site.register(Pago)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Rubro)
admin.site.register(Subcategoria)
admin.site.register(Tipopago)
admin.site.register(Venta)
admin.site.register(VentaProducto)
