# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.contrib.auth.models import User


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    def __str__(self):
        return f'{self.username}'

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Boleta(models.Model):
    idboleta = models.AutoField(db_column='IdBoleta', primary_key=True)  # Field name made lowercase.
    fechaboleta = models.DateTimeField(db_column='FechaBoleta')  # Field name made lowercase.
    subtotalboleta = models.IntegerField(db_column='SubTotalBoleta')  # Field name made lowercase.
    ivaboleta = models.DecimalField(db_column='IVABoleta', max_digits=10, decimal_places=0)  # Field name made lowercase.
    totalboleta = models.DecimalField(db_column='TotalBoleta', max_digits=10, decimal_places=0)  # Field name made lowercase.
    idventa = models.ForeignKey('Venta', models.DO_NOTHING, db_column='IdVenta')  # Field name made lowercase.

    def __str__(self):
        return f'{self.idboleta} {self.fechaboleta} Total:{self.totalboleta}'

    class Meta:
        managed = False
        db_table = 'boleta'


class Categoria(models.Model):
    idcategoria = models.AutoField(db_column='IdCategoria', primary_key=True)  # Field name made lowercase.
    nombrecategoria = models.CharField(db_column='NombreCategoria', max_length=50)  # Field name made lowercase.

    def __str__(self):
        return f'{self.idcategoria} {self.nombrecategoria}'

    class Meta:
        managed = False
        db_table = 'categoria'


class Despacho(models.Model):
    iddespacho = models.AutoField(db_column='IdDespacho', primary_key=True)  # Field name made lowercase.
    fechainicio = models.DateTimeField(db_column='FechaInicio')  # Field name made lowercase.
    fechatermino = models.DateTimeField(db_column='FechaTermino', blank=True, null=True)  # Field name made lowercase.
    direcciondestino = models.CharField(db_column='DireccionDestino', max_length=100)  # Field name made lowercase.
    idventa = models.ForeignKey('Venta', models.DO_NOTHING, db_column='IdVenta')  # Field name made lowercase.
    idestadodespacho = models.ForeignKey('Estadodespacho', models.DO_NOTHING, db_column='IdEstadoDespacho')  # Field name made lowercase.

    def __str__(self):
        return f'{self.iddespacho} {self.fechainicio} {self.fechatermino}'

    class Meta:
        managed = False
        db_table = 'despacho'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Estadodespacho(models.Model):
    idestadodespacho = models.IntegerField(db_column='IdEstadoDespacho', primary_key=True)  # Field name made lowercase.
    nombreestadodespacho = models.CharField(db_column='NombreEstadoDespacho', max_length=50)  # Field name made lowercase.

    def __str__(self):
        return f'{self.nombreestadodespacho}'

    class Meta:
        managed = False
        db_table = 'estadodespacho'


class Estadoordencompra(models.Model):
    idestadooc = models.IntegerField(db_column='IdEstadoOC', primary_key=True)  # Field name made lowercase.
    nombreestadooc = models.CharField(db_column='NombreEstadoOC', max_length=50)  # Field name made lowercase.

    def __str__(self):
        return f'{self.nombreestadooc}'

    class Meta:
        managed = False
        db_table = 'estadoordencompra'


class Estadopago(models.Model):
    idestadopago = models.IntegerField(db_column='IdEstadoPago', primary_key=True)  # Field name made lowercase.
    nombreestadopago = models.CharField(db_column='NombreEstadoPago', max_length=50)  # Field name made lowercase.

    def __str__(self):
        return f'{self.nombreestadopago}'

    class Meta:
        managed = False
        db_table = 'estadopago'


class Estadoventa(models.Model):
    idestadoventa = models.IntegerField(db_column='IdEstadoVenta', primary_key=True)  # Field name made lowercase.
    nombreestadoventa = models.CharField(db_column='NombreEstadoVenta', max_length=50)  # Field name made lowercase.

    def __str__(self):
        return f'{self.nombreestadoventa}'

    class Meta:
        managed = False
        db_table = 'estadoventa'


class Factura(models.Model):
    idfactura = models.AutoField(db_column='IdFactura', primary_key=True)  # Field name made lowercase.
    fechafactura = models.DateTimeField(db_column='FechaFactura')  # Field name made lowercase.
    subtotalfactura = models.IntegerField(db_column='SubTotalFactura')  # Field name made lowercase.
    ivafactura = models.DecimalField(db_column='IVAFactura', max_digits=10, decimal_places=0)  # Field name made lowercase.
    totalfactura = models.DecimalField(db_column='TotalFactura', max_digits=10, decimal_places=0)  # Field name made lowercase.
    rutempresa = models.CharField(db_column='RutEmpresa', max_length=12)  # Field name made lowercase.
    idventa = models.ForeignKey('Venta', models.DO_NOTHING, db_column='IdVenta')  # Field name made lowercase.

    def __str__(self):
        return f'{self.idfactura} {self.fechafactura} Total:{self.totalfactura}'

    class Meta:
        managed = False
        db_table = 'factura'


class Ordencompra(models.Model):
    idordencompra = models.AutoField(db_column='IdOrdenCompra', primary_key=True)  # Field name made lowercase.
    fecha = models.DateTimeField(db_column='Fecha')  # Field name made lowercase.
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='IdUsuario')  # Field name made lowercase.
    idestadooc = models.ForeignKey(Estadoordencompra, models.DO_NOTHING, db_column='IdEstadoOC')  # Field name made lowercase.
    idproveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='IdProveedor')  # Field name made lowercase.
    comentarios = models.CharField(db_column='Comentarios', max_length=500, blank=True, null=True)  # Field name made lowercase.
    
    def __str__(self):
        return f'{self.idordencompra} {self.fecha}'

    class Meta:
        managed = False
        db_table = 'ordencompra'


class OrdencompraProducto(models.Model):
    idproducto = models.OneToOneField('Producto', models.DO_NOTHING, db_column='IdProducto', primary_key=True)  # Field name made lowercase.
    idordencompra = models.ForeignKey(Ordencompra, models.DO_NOTHING, db_column='IdOrdenCompra')  # Field name made lowercase.
    cantidadoc = models.IntegerField(db_column='CantidadOC')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ordencompra_producto'
        unique_together = (('idproducto', 'idordencompra'),)


class Pago(models.Model):
    idpago = models.AutoField(db_column='IdPago', primary_key=True)  # Field name made lowercase.
    monto = models.IntegerField(db_column='Monto')  # Field name made lowercase.
    fechapago = models.DateTimeField(db_column='FechaPago')  # Field name made lowercase.
    idventa = models.ForeignKey('Venta', models.DO_NOTHING, db_column='IdVenta')  # Field name made lowercase.
    idtipopago = models.ForeignKey('Tipopago', models.DO_NOTHING, db_column='IdTipoPago')  # Field name made lowercase.
    idestadopago = models.ForeignKey(Estadopago, models.DO_NOTHING, db_column='IdEstadoPago')  # Field name made lowercase.
    
    def __str__(self):
        return f'{self.idpago} {self.monto} {self.fechapago}'

    class Meta:
        managed = False
        db_table = 'pago'


class Producto(models.Model):
    idproducto = models.BigIntegerField(db_column='IdProducto', primary_key=True)  # Field name made lowercase.
    nombreproducto = models.CharField(db_column='NombreProducto', max_length=100)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=500)  # Field name made lowercase.
    stock = models.IntegerField(db_column='Stock')  # Field name made lowercase.
    stockcritico = models.IntegerField(db_column='StockCritico')  # Field name made lowercase.
    precio = models.IntegerField(db_column='Precio')  # Field name made lowercase.
    marca = models.CharField(db_column='Marca', max_length=50)  # Field name made lowercase.
    fechavencimiento = models.DateTimeField(db_column='FechaVencimiento', blank=True, null=True)  # Field name made lowercase.
    idsubcategoria = models.ForeignKey('Subcategoria', models.DO_NOTHING, db_column='IdSubCategoria')  # Field name made lowercase.
    idproveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='IdProveedor')  # Field name made lowercase.
    foto = models.ImageField(db_column='Foto', max_length=500, blank=True, null=True, default='product-1.jpg')  # Field name made lowercase.

    def __str__(self):
        return f'Codigo:{self.idproducto} {self.nombreproducto}'

    class Meta:
        managed = False
        db_table = 'producto'


class Proveedor(models.Model):
    idproveedor = models.AutoField(db_column='IdProveedor', primary_key=True)  # Field name made lowercase.
    rutproveedor = models.CharField(db_column='RutProveedor', max_length=12)  # Field name made lowercase.
    nombreproveedor = models.CharField(db_column='NombreProveedor', max_length=100)  # Field name made lowercase.
    telefono = models.IntegerField(db_column='Telefono')  # Field name made lowercase.
    correo = models.CharField(db_column='Correo', max_length=100)  # Field name made lowercase.
    idrubro = models.ForeignKey('Rubro', models.DO_NOTHING, db_column='IdRubro')  # Field name made lowercase.

    def __str__(self):
        return f'Id:{self.idproveedor} {self.nombreproveedor}'

    class Meta:
        managed = False
        db_table = 'proveedor'

class Rubro(models.Model):
    idrubro = models.IntegerField(db_column='IdRubro', primary_key=True)  # Field name made lowercase.
    nombrerubro = models.CharField(db_column='NombreRubro', max_length=150)  # Field name made lowercase.

    def __str__(self):
        return f'{self.nombrerubro}'

    class Meta:
        managed = False
        db_table = 'rubro'


class Subcategoria(models.Model):
    idsubcategoria = models.AutoField(db_column='IdSubCategoria', primary_key=True)  # Field name made lowercase.
    nombresubcategoria = models.CharField(db_column='NombreSubCategoria', max_length=50)  # Field name made lowercase.
    idcategoria = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='IdCategoria')  # Field name made lowercase.

    def __str__(self):
        return f'{self.idsubcategoria} {self.nombresubcategoria}-{self.idcategoria}'

    class Meta:
        managed = False
        db_table = 'subcategoria'


class Tipopago(models.Model):
    idtipopago = models.IntegerField(db_column='IdTipoPago', primary_key=True)  # Field name made lowercase.
    nombretipopago = models.CharField(db_column='NombreTipoPago', max_length=50)  # Field name made lowercase.

    def __str__(self):
        return f'{self.nombretipopago}'

    class Meta:
        managed = False
        db_table = 'tipopago'


class Usuario(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    rut = models.CharField(db_column='Rut', max_length=12, blank=True, null=True)  # Field name made lowercase.
    correo = models.CharField(db_column='Correo', max_length=100)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=True, null=True)  # Field name made lowercase.
    apellido = models.CharField(db_column='Apellido', max_length=50, blank=True, null=True)  # Field name made lowercase.
    telefono = models.IntegerField(db_column='Telefono', blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=100, blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='User', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return f'{self.correo} {self.nombre} {self.apellido}'

    class Meta:
        managed = False
        db_table = 'usuario'


class Venta(models.Model):
    idventa = models.AutoField(db_column='IdVenta', primary_key=True)  # Field name made lowercase.
    fechaventa = models.DateTimeField(db_column='FechaVenta')  # Field name made lowercase.
    idusuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='IdUsuario')  # Field name made lowercase.
    idestadoventa = models.ForeignKey(Estadoventa, models.DO_NOTHING, db_column='IdEstadoVenta')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'venta'


class VentaProducto(models.Model):
    idproducto = models.OneToOneField(Producto, models.DO_NOTHING, db_column='IdProducto', primary_key=True)  # Field name made lowercase.
    idventa = models.ForeignKey(Venta, models.DO_NOTHING, db_column='IdVenta')  # Field name made lowercase.
    cantidadproducto = models.IntegerField(db_column='CantidadProducto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'venta_producto'
        unique_together = (('idproducto', 'idventa'),)
