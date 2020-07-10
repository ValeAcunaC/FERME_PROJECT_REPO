import os
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import *
from .decorators import *
from .filters import *

from django.http import JsonResponse
import json

from datetime import datetime


visitas = 0
def index(request):
    productos = Producto.objects.all()
    subcategorias = Subcategoria.objects.all()
    categorias = Categoria.objects.all()
    global visitas
    visitas = visitas + 1

    #mejorar
    if request.user.is_authenticated:
        id = request.user.id
        usuario = Usuario.objects.get(user = id)
        estado = Estadoventa.objects.get(idestadoventa= 1)
        venta, created = Venta.objects.get_or_create(idusuario= usuario, idestadoventa= estado)
        items = venta.ventaproducto_set.all()
    else:
        venta= []
        items = []
    #mejorar


    # global num_visits
    # num_visits = request.session.get('num_visits',0)
    # num_visits=request.session['num_visits']=num_visits+1
    context={'productos': productos, 'subcategorias': subcategorias, 'categorias': categorias,'venta':venta, 'items':items}
    return render(request,'index.html',context)

def detalleProducto(request, pk):
    producto = Producto.objects.get(idproducto=pk)

    #mejorar
    if request.user.is_authenticated:
        id = request.user.id
        usuario = Usuario.objects.get(user = id)
        estado = Estadoventa.objects.get(idestadoventa= 1)
        venta, created = Venta.objects.get_or_create(idusuario= usuario, idestadoventa= estado)
        items = venta.ventaproducto_set.all()
    else:
        venta= []
        items = []
    #mejorar

    context = {'item':producto,'categorias': categorias,'venta':venta, 'items':items}
    return render(request,'detalle-producto.html',context)

#account
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Email o Contraseña incorrecta')

    context = {}
    return render(request,'account/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('index')

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data.get('username')

            u = User.objects.get(username=username)
            u.email = u.username

            group = request.POST.get('empresa')
            if group != 'empresa':
                group = 'persona'
            g = Group.objects.get(name=group)
            u.groups.add(g)
            u.save()

            au = AuthUser.objects.get(username=username)

            usuario = Usuario(correo=u.email,user=au)
            usuario.save()
            
            messages.success(request, 'Cuenta creada con exito para: ' +username+', ahora solo falta que llenes tu información personal')
            login(request, u)
            return redirect('perfil/'+str(u.id))

    context = {'form':form}
    return render(request,'account/register.html',context)

@login_required(login_url='login')
def perfil(request, pk):
    user = User.objects.get(id=pk)

    u = request.user.id
    if u != pk:
        return redirect('index')

    usuario = Usuario.objects.get(user_id=u)

    form = UsuarioForm(instance=user)
    #context= {'form':form}
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()

    #mejorar
    if request.user.is_authenticated:
        estado = Estadoventa.objects.get(idestadoventa= 1)
        venta, created = Venta.objects.get_or_create(idusuario= usuario, idestadoventa= estado)
        items = venta.ventaproducto_set.all()
    else:
        venta= []
        items = []
    #mejorar

    context= {'form':form,'categorias': categorias,'venta':venta, 'items':items}        
    return render(request, 'account/perfil.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','vendedor','persona','empresa'])
def miscompras(request):
    return render(request,'account/miscompras.html')

#pageinfo
def contacto(request):
    return render(request,'pageinfo/contacto.html')

def faq(request):
    return render(request,'pageinfo/faq.html')

def terminosycondiciones(request):
    return render(request,'pageinfo/terminos-y-condiciones.html')

def nosotros(request):
    return render(request,'pageinfo/nosotros.html')



#crud tablas
@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def productos(request):
    productos = Producto.objects.all()
    subcategorias = Subcategoria.objects.all()

    myFilter = ProductoFilter(request.GET, queryset=productos)
    productos = myFilter.qs

    return render(request,'cruds/tabla-productos.html', {'productos': productos, 'subcategorias': subcategorias, 'myFilter':myFilter})

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def categorias(request):
    categorias = Categoria.objects.all()

    myFilter = CategoriaFilter(request.GET, queryset=categorias)
    categorias = myFilter.qs

    return render(request,'cruds/tabla-categorias.html', {'categorias': categorias, 'myFilter':myFilter})

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def subcategorias(request):
    subcategorias = Subcategoria.objects.all()

    myFilter = SubcategoriaFilter(request.GET, queryset=subcategorias)
    subcategorias = myFilter.qs

    return render(request,'cruds/tabla-subcategorias.html', {'subcategorias': subcategorias, 'myFilter':myFilter})

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def proveedores(request):
    proveedores = Proveedor.objects.all()

    myFilter = ProveedorFilter(request.GET, queryset=proveedores)
    proveedores = myFilter.qs

    return render(request,'cruds/tabla-proveedores.html', {'proveedores': proveedores, 'myFilter':myFilter})

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def ordenes(request):
    ordenes = Ordencompra.objects.all()
    return render(request,'cruds/tabla-ordenes.html', {'ordenes': ordenes})
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador'])
def usuarios(request):
    usuarios = User.objects.filter(is_staff=True).filter(is_active=True)
    #empleados = User.objects.filter(groups__name='empleado')

    myFilter = UserFilter(request.GET, queryset=usuarios)
    usuarios = myFilter.qs

    return render(request,'cruds/tabla-usuarios.html', {'usuarios': usuarios, 'myFilter':myFilter})

#crud categoria
@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def crearCategoria(request):
    form = CategoriaForm()
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias')

    context = {'form':form}
    return render(request,'cruds/categoria.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def modificarCategoria(request, pk):
    categoria = Categoria.objects.get(idcategoria=pk)
    form = CategoriaForm(instance=categoria)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categorias')

    context = {'form':form}
    return render(request,'cruds/categoria.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def eliminarCategoria(request, pk):
    categoria = Categoria.objects.get(idcategoria=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categorias')
        
    context = {'item':categoria}
    return render(request,'cruds/eliminar_categoria.html',context)

#crud subcategoria
@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def crearSubcategoria(request):
    form = SubcategoriaForm()
    if request.method == 'POST':
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subcategorias')

    context = {'form':form}
    return render(request,'cruds/subcategoria.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def modificarSubcategoria(request, pk):
    subcategoria = Subcategoria.objects.get(idsubcategoria=pk)
    form = SubcategoriaForm(instance=subcategoria)

    if request.method == 'POST':
        form = SubcategoriaForm(request.POST, instance=subcategoria)
        if form.is_valid():
            form.save()
            return redirect('subcategorias')

    context = {'form':form}
    return render(request,'cruds/subcategoria.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def eliminarSubcategoria(request, pk):
    subcategoria = Subcategoria.objects.get(idsubcategoria=pk)
    if request.method == 'POST':
        subcategoria.delete()
        return redirect('subcategorias')
        
    context = {'item':subcategoria}
    return render(request,'cruds/eliminar-subcategoria.html',context)

#crud usuario
@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador'])
def crearUsuario(request):
    form = StaffForm()
    empleado = False
    vendedor = False
    administrador = False
    if request.method == 'POST':
        form = StaffForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            u = User.objects.get(username=username)
            u.email = u.username

            emp = request.POST.get('empleado')
            g_emp = Group.objects.get(name='empleado')
            if emp == 'empleado':
                u.groups.add(g_emp)

            ven = request.POST.get('vendedor')
            if ven == 'vendedor':
                g_ven = Group.objects.get(name='vendedor')
                u.groups.add(g_ven)

            adm = request.POST.get('administrador')
            if adm == 'administrador':
                g_adm = Group.objects.get(name='administrador')
                u.groups.add(g_adm)

            u.set_password(u.password)
            u.save()

            au = AuthUser.objects.get(username=username)

            usuario = Usuario(correo=u.email,user=au)
            usuario.save()

            return redirect('usuarios')

    context = {'form':form,'empleado':empleado,'vendedor':vendedor,'administrador':administrador}
    return render(request,'cruds/usuario.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador'])
def modificarUsuario(request, pk):
    u = User.objects.get(id=pk)
    form = StaffForm(instance=u)
    empleado = False
    vendedor = False
    administrador = False

    if u.groups.filter(name='empleado').exists():
        empleado = True
    if u.groups.filter(name='vendedor').exists():
        vendedor = True
    if u.groups.filter(name='administrador').exists():
        administrador = True
    
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=u)
        if form.is_valid():

            emp = request.POST.get('empleado')
            g_emp = Group.objects.get(name='empleado')
            if emp == 'empleado':
                u.groups.add(g_emp)
            else:
                if empleado:
                    g_emp.user_set.remove(u)

            ven = request.POST.get('vendedor')
            g_ven = Group.objects.get(name='vendedor')
            if ven == 'vendedor':
                u.groups.add(g_ven)
            else:
                if vendedor:
                    g_ven.user_set.remove(u)

            adm = request.POST.get('administrador')
            g_adm = Group.objects.get(name='administrador')
            if adm == 'administrador':
                u.groups.add(g_adm)
            else:
                if administrador:
                    g_adm.user_set.remove(u)

            u.set_password(u.password)    
            u.save()

            form.save()
            return redirect('usuarios')

    context = {'form':form,'empleado':empleado,'vendedor':vendedor,'administrador':administrador}
    return render(request,'cruds/usuario.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador'])
def eliminarUsuario(request, pk):
    usuario = User.objects.get(id=pk)
    if request.method == 'POST':
        usuario.is_active = 0
        usuario.save()
        return redirect('usuarios')
        
    context = {'item':usuario}
    return render(request,'cruds/eliminar-usuario.html',context)

#crud proveedores
@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def crearProveedor(request):
    form = ProveedorForm()
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedores')

    context = {'form':form}
    return render(request,'cruds/proveedor.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def modificarProveedor(request, pk):
    proveedor = Proveedor.objects.get(idproveedor=pk)
    form = ProveedorForm(instance=proveedor)

    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedores')

    context = {'form':form}
    return render(request,'cruds/proveedor.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def eliminarProveedor(request, pk):
    proveedor = Proveedor.objects.get(idproveedor=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedores')
        
    context = {'item':proveedor}
    return render(request,'cruds/eliminar-proveedor.html',context)

#crud Producto
@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def crearProducto(request):
    form = ProductoForm()
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productos')

    context = {'form':form}
    return render(request,'cruds/producto.html',context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['administrador','empleado'])
# def modificarProducto(request, pk):
#     producto = Producto.objects.get(idproducto=pk)
#     form = ProductoForm(instance=producto)

#     if request.method == 'POST':
#         form = ProductoForm(request.POST, request.FILES, instance=producto)
#         if form.is_valid():
#             form.save()
#             return redirect('productos')

#     context = {'form':form}
#     return render(request,'cruds/producto.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def modificarProducto(request, pk):
    producto = Producto.objects.get(idproducto=pk)
    form = ModificarProductoForm(instance=producto)

    if request.method == 'POST':
        form = ModificarProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos')

    context = {'form':form}
    return render(request,'cruds/modificar-producto.html',context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def eliminarProducto(request, pk):
    producto = Producto.objects.get(idproducto=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos')
        
    context = {'item':producto}
    return render(request,'cruds/eliminar-producto.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','vendedor'])
def ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas.html', {'ventas': ventas})

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador'])
def dashboard(request):
    #num_visits=request.session.get('num_visits',0)
    #num_visits=request.session['num_visits']=num_visits+1
    global visitas
    personas = User.objects.filter(groups__name='persona')
    total_personas = personas.count()
    empresas = User.objects.filter(groups__name='empresa')
    total_empresas = empresas.count()
    total_productos = Producto.objects.count()
    context={'total_personas': total_personas,'total_empresas': total_empresas, 'total_productos': total_productos,'num_visits':visitas,}
    return render(request, 'dashboard.html', context)


#crud ordencompra
@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def crearOrdencompra(request):
    u = request.user.id
    usuario = Usuario.objects.get(user=u)
    estadocreado = Estadoordencompra.objects.get(nombreestadooc="Creado")
    #form = OrdencompraForm(usuario = usuario.id, estadocreado = estadocreado.idestadooc)
    
    #ids = [usuario.id, estadocreado.idestadooc]
    #form = OrdencompraForm(usuario = usuario.id,estadocreado = estadocreado.idestadooc)
    form = OrdencompraForm()
    if request.method == 'POST':
        form = OrdencompraForm(request.POST)
        
        if form.is_valid():
            form.save()
            idordencompra = Ordencompra.objects.latest('idordencompra')
            #print("id orden: ",str(idordencompra))
            #ordencompra = Ordencompra.objects.get(idordencompra=idordencompra)
            #ordencompra = ordencompra.idordencompra
            #print("id orden: ",idordencompra)
            return redirect('detalle_ordencompra/'+str(idordencompra))

    context = {'form':form,'usuario':usuario.id,'estadocreado':estadocreado}
    return render(request,'cruds/ordencompra.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def modificarOrdencompra(request, pk):
    ordencompra = Ordencompra.objects.get(idordencompra=pk)
    form = OrdencompraForm(instance=ordencompra)
    if request.method == 'POST':
        form = OrdencompraForm(request.POST, instance=ordencompra)
        if form.is_valid():
            form.save()
            return redirect('ordenes')

    context = {'form':form}
    return render(request,'cruds/ordencompra.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','empleado'])
def eliminarOrdencompra(request, pk):
    ordencompra = Ordencompra.objects.get(idordencompra=pk)
    if request.method == 'POST':
        ordencompra.delete()
        return redirect('ordenes')
        
    context = {'item':ordencompra}
    return render(request,'cruds/eliminar-ordencompra.html',context)

#crud ordencompraproducto
def crearOrdencompraproducto(request, pk):
    ordencompra = Ordencompra.objects.get(idordencompra=pk)
    form = OrdencompraproductoForm()
    if OrdencompraProducto.objects.filter(idordencompra=pk).exists():
        ordencompraproducto = OrdencompraProducto.objects.filter(idordencompra=pk)
    else:
        ordencompraproducto = False
    
    if request.method == 'POST':
        form = OrdencompraproductoForm(request.POST)
        if form.is_valid():
            form.save()
            #idordencompra = form.cleaned_data.get('idordencompra')
            #idordencompra = OrdencompraProducto.objects.latest('idordencompra')
            #return redirect('crear_ordencompraproducto/'+str(idordencompra))
    
    context = {'item':ordencompra, 'ordencompraproducto':ordencompraproducto,'form':form}
    return render(request,'cruds/ordencompraproducto.html',context)

def modificarOrdencompraproducto(request, pk):
    ordencompraproducto = OrdencompraProducto.objects.get(idocp=pk)
    ordencompra = Ordencompra.objects.get(idordencompra=ordencompraproducto.idordencompra.idordencompra)
    form = OrdencompraproductoForm(instance=ordencompraproducto)
    if request.method == 'POST':
        form = OrdencompraproductoForm(request.POST, instance=ordencompraproducto)
        if form.is_valid():
            form.save()

    if OrdencompraProducto.objects.filter(idordencompra=ordencompra.idordencompra).exists():
        ordencompraproducto = OrdencompraProducto.objects.filter(idordencompra=ordencompra.idordencompra)
    else:
        ordencompraproducto = False
    
    context = {'item':ordencompra, 'ordencompraproducto':ordencompraproducto,'form':form}
    return render(request,'cruds/ordencompraproducto.html',context)

def eliminarOrdencompraproducto(request, pk):
    ordencompraproducto = OrdencompraProducto.objects.get(idocp=pk)
    idoc = ordencompraproducto.idordencompra
    print(idoc)
    if request.method == 'POST':
        ordencompraproducto.delete()
        return redirect('detalle_ordencompra/'+str(idoc))
        
    context = {'item':ordencompraproducto}
    return render(request,'cruds/eliminar-ordencompraproducto.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','vendedor','persona','empresa'])
def carro(request):
    #mejorar
    if request.user.is_authenticated:
        id = request.user.id
        usuario = Usuario.objects.get(user = id)
        estado = Estadoventa.objects.get(idestadoventa= 1)
        venta, created = Venta.objects.get_or_create(idusuario= usuario, idestadoventa= estado)
        items = venta.ventaproducto_set.all()
    else:
        venta= []
        items = []
    #mejorar
    context = {'items':items,'venta':venta}
    return render(request, 'carro.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:',productId)
    
    id = request.user.id
    usuario = Usuario.objects.get(user = id)
    producto = Producto.objects.get(idproducto=productId)
    venta, created = Venta.objects.get_or_create(idusuario= usuario.id, idestadoventa= 1)

    orderItem, created = VentaProducto.objects.get_or_create(idproducto= producto, idventa= venta)

    if action == 'add':
        if (orderItem.cantidadproducto + 1)<= producto.stock:
            orderItem.cantidadproducto = (orderItem.cantidadproducto + 1)
        else:
            messages.info(request, 'Stock insuficiente')
    elif action == 'remove':
        orderItem.cantidadproducto = (orderItem.cantidadproducto - 1)
    elif action == 'delete':
        orderItem.cantidadproducto = 0

    orderItem.save()
    if orderItem.cantidadproducto <= 0:
        orderItem.delete()
    return JsonResponse('Item was updated', safe=False)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','vendedor','persona','empresa'])
def checkout(request):
    #mejorar
    if request.user.is_authenticated:
        id = request.user.id
        usuario = Usuario.objects.get(user = id)
        estado = Estadoventa.objects.get(idestadoventa= 1)
        venta, created = Venta.objects.get_or_create(idusuario= usuario, idestadoventa= estado)
        items = venta.ventaproducto_set.all()
    else:
        venta= []
        items = []
    #mejorar

    if request.user.groups.filter(name='persona').exists() or request.user.groups.filter(name='empresa').exists():
        dirDespacho = usuario.direccion
    else:
        dirDespacho = ''

    if request.method == 'POST':

        direccion = request.POST.get('direccion')
        asd = request.POST.get('despacho')
        if (asd == 'despacho' and direccion=='') or ((request.user.groups.filter(name='persona').exists() or request.user.groups.filter(name='empresa').exists()) and direccion==''):
            messages.info(request, 'Debe ingresar la direccion de despacho')
            context = {'items':items,'venta':venta,'dirDespacho':dirDespacho}
            return render(request, 'checkout.html', context)

        if direccion is not None:
            estado = Estadodespacho.objects.get(idestadodespacho=1)
            despacho = Despacho(direcciondestino=direccion,idventa=venta,idestadodespacho=estado)
            despacho.save()

        monto = request.POST.get('monto')

        array = VentaProducto.objects.filter(idventa=venta.idventa)
        producto = None

        for i in array:
            producto = Producto.objects.get(idproducto=i.idproducto.idproducto)
            if 0 > (producto.stock - i.cantidadproducto):
                messages.info(request, 'Stock de articulos insuficiente')
                context = {'items':items,'venta':venta,'dirDespacho':dirDespacho}
                return render(request, 'checkout.html', context)

        if request.user.groups.filter(name='vendedor').exists() or request.user.groups.filter(name='administrador').exists():
            estadoV = Estadoventa.objects.get(idestadoventa=3)
            venta.idestadoventa = estadoV
            venta.fechaventa = datetime.now()
            venta.save()

            for i in array:
                producto = Producto.objects.get(idproducto=i.idproducto.idproducto)
                producto.stock = producto.stock - i.cantidadproducto
                producto.save()


            return redirect('recibo/'+str(venta.idventa)+'/'+str(monto))
        else:
            estadoPago = Estadopago.objects.get(idestadopago=1)
            pago = Pago(monto=monto, idventa=venta, idestadopago=estadoPago)
            pago.save()

        return redirect('tbkinit/'+str(pago.idpago))

    context = {'items':items,'venta':venta,'dirDespacho':dirDespacho}
    return render(request, 'checkout.html', context)

#TBK Section
from django.views.decorators.csrf import csrf_exempt

from .tbk import tbk
from .tbk.tbk.services import WebpayService
from .tbk.tbk.commerce import Commerce
from .tbk.tbk import INTEGRACION
import flask
import logging
import random

CERTIFICATES_DIR = os.path.join(os.path.dirname(__file__), "commerces")

def load_commerce_data(commerce_code):
    with open(
        os.path.join(CERTIFICATES_DIR, commerce_code, commerce_code + ".key"), "r"
    ) as file:
        key_data = file.read()
    with open(
        os.path.join(CERTIFICATES_DIR, commerce_code, commerce_code + ".crt"), "r"
    ) as file:
        cert_data = file.read()
    with open(os.path.join(CERTIFICATES_DIR, "tbk.pem"), "r") as file:
        tbk_cert_data = file.read()

    return {
        "key_data": key_data,
        "cert_data": cert_data,
        "tbk_cert_data": tbk_cert_data,
    }

app = flask.Flask(__name__)
app.secret_key = "TBKSESSION"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logging.getLogger("tbk").setLevel(logging.DEBUG)

HOST = os.getenv("HOST", "http://localhost")
PORT = os.getenv("PORT", 5000)
BASE_URL = "{host}:{port}".format(host=HOST, port=PORT)

NORMAL_COMMERCE_CODE = "597020000541"
ONECLICK_COMMERCE_CODE = "597020000593"

normal_commerce_data = load_commerce_data(NORMAL_COMMERCE_CODE)
normal_commerce = tbk.commerce.Commerce(
    commerce_code=NORMAL_COMMERCE_CODE,
    key_data=normal_commerce_data["key_data"],
    cert_data=normal_commerce_data["cert_data"],
    tbk_cert_data=normal_commerce_data["tbk_cert_data"],
    environment=tbk.environments.DEVELOPMENT,
)
webpay_service = tbk.services.WebpayService(normal_commerce)

oneclick_commerce_data = load_commerce_data(ONECLICK_COMMERCE_CODE)
oneclick_commerce = tbk.commerce.Commerce(
    commerce_code=ONECLICK_COMMERCE_CODE,
    key_data=oneclick_commerce_data["key_data"],
    cert_data=oneclick_commerce_data["cert_data"],
    tbk_cert_data=oneclick_commerce_data["tbk_cert_data"],
    environment=tbk.environments.DEVELOPMENT,
)

oneclick_service = tbk.services.OneClickPaymentService(oneclick_commerce)
oneclick_commerce_service = tbk.services.CommerceIntegrationService(oneclick_commerce)

@csrf_exempt
def tbkinit(request, pk):

    pago = Pago.objects.get(idpago=pk)

    transaction = webpay_service.init_transaction(
    amount=pago.monto,
    buy_order=pk,
    return_url="http://127.0.0.1:8000/tbkresponse",
    final_url="http://127.0.0.1:8000/tbkfinal",
    session_id=request.user.id)
    # print('token:'+ transaction['token'])
    # print('url:'+ transaction['url'])
    
    token = transaction['token']
    pago.token = token
    pago.save()

    context = {'token_ws':token, 'action':transaction['url']}
    return render(request,'tbkinit.html',context)

@csrf_exempt
def tbkresponse(request):
    token_ws = request.POST.get('token_ws')

    transaction = webpay_service.get_transaction_result(token_ws)
    transaction_detail = transaction["detailOutput"][0]
    url = transaction['urlRedirection']
    print('detail:',transaction_detail)

    estado = 3
    if transaction_detail["responseCode"] == 0:
        estado = 2

    estadoPago = Estadopago.objects.get(idestadopago=estado)
    estadoVenta = Estadoventa.objects.get(idestadoventa=estado)

    fechaHora = datetime.now()

    pago = Pago.objects.get(token=token_ws)
    pago.idestadopago = estadoPago
    pago.fechapago = fechaHora
    pago.save()
    venta = Venta.objects.get(idventa= pago.idventa.idventa)
    venta.idestadoventa = estadoVenta
    venta.fechaventa = fechaHora
    venta.save()

    subtotal = pago.monto * 0.81
    iva = pago.monto * 0.19

    u = User.objects.get(id=venta.idusuario.user.id)

    if u.groups.filter(name='empresa').exists():
        factura = Factura(fechafactura=fechaHora, subtotalfactura=subtotal, ivafactura=iva, totalfactura= pago.monto, rutempresa=pago.idusuario.rut, idventa=venta)
        factura.save()
    else:
        boleta = Boleta(fechaboleta=fechaHora, subtotalboleta=subtotal, ivaboleta=iva, totalboleta= pago.monto, idventa=venta)
        boleta.save()

    array = VentaProducto.objects.filter(idventa=venta.idventa)
    producto = None
    for i in array:
        producto = Producto.objects.get(idproducto=i.idproducto.idproducto)
        producto.stock = producto.stock - i.cantidadproducto
        producto.save()

    webpay_service.acknowledge_transaction(token_ws)

    context = {'token_ws':token_ws, 'url':url}
    return render(request,'tbkresponse.html',context)

@csrf_exempt
def tbkfinal(request):
    token_ws = request.POST.get('token_ws')
    pago = Pago.objects.get(token=token_ws)

    return redirect('comprobante/'+str(pago.idpago))

def comprobante(request,pk):
    pago = Pago.objects.get(idpago=pk)
    productos = VentaProducto.objects.filter(idventa=pago.idventa.idventa)
    despacho = Despacho.objects.get(idventa=pago.idventa.idventa)
    if request.user.groups.filter(name='persona').exists():
        comprobante = Boleta.objects.get(idventa=pago.idventa.idventa)
        fecha = comprobante.fechaboleta
        subtotal = comprobante.subtotalboleta
        iva = comprobante.ivaboleta
        total = comprobante.totalboleta
    if request.user.groups.filter(name='empresa').exists():
        comprobante = Factura.objects.get(idventa=pago.idventa.idventa)
        fecha = comprobante.fechafactura
        subtotal = comprobante.subtotalfactura
        iva = comprobante.ivafactura
        total = comprobante.totalfactura
    context = {'pago':pago, 'productos':productos, 'fecha': fecha, 'subtotal': subtotal, 'iva': iva, 'total': total, 'despacho': despacho}
    return render(request,'comprobante.html',context)

def recibo(request,pk,monto):
    fecha = datetime.now()
    subtotal = round(float(monto) *0.81)
    iva = round(float(monto)*0.19)
    venta = Venta.objects.get(idventa=pk)

    if request.method == 'POST':
        
        rut = request.POST.get('rutempresa')
        asd = request.POST.get('factura')
        if asd == 'factura' and rut == '':
            context = {'monto':monto,'iva':iva,'subtotal':subtotal,'fecha':fecha}
            return render(request,'recibo.html',context)
        if rut is None or rut == "":
            boleta = Boleta(fechaboleta=fecha, subtotalboleta=subtotal, ivaboleta=iva, totalboleta=monto, idventa=venta)
            boleta.save()
        else:
            factura = Factura(fechafactura=fecha, subtotalfactura=subtotal, ivafactura=iva, totalfactura=monto, rutempresa=venta.idusuario.rut, idventa=venta)
            factura.save()

        return redirect('venta_fin')


    context = {'monto':monto,'iva':iva,'subtotal':subtotal,'fecha':fecha}
    return render(request,'recibo.html',context)

def ventaFin(request):
    return render(request,'venta-fin.html')

def misCompras(request):
    usuario = Usuario.objects.get(user=request.user.id)
    ventas = Venta.objects.filter(idusuario=usuario.id).exclude(idestadoventa=1)
    array = []
    for i in ventas:
        despacho = Despacho.objects.get(idventa=i.idventa)
        if despacho.idventa.idventa == i.idventa:
            array.append(despacho)

    context = {'array':array}
    return render(request,'mis-compras.html',context)

def detalleCompra(request,pk):
    detalle = VentaProducto.objects.filter(idventa=pk)
    context = {'detalle':detalle}
    return render(request,'detalle-compra.html',context)

