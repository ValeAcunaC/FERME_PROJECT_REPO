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

from .filters import *



def index(request):
    productos = Producto.objects.all()
    subcategorias = Subcategoria.objects.all()
    return render(request,'index.html', {'productos': productos, 'subcategorias': subcategorias})

def producto(request):
    # rubro = Rubro.objects.get(idrubro=3)
    # newProveedor = Proveedor(rutproveedor='7-8',nombreproveedor='proveedor3',telefono=123456789,correo='proveedor3@correo.cl',idrubro=rubro)
    # newProveedor.save()
    return render(request,'producto.html')

def detalleProducto(request, pk):
    producto = Producto.objects.get(idproducto=pk)
    context = {'item':producto}
    return render(request,'detalle-producto.html',context)

#account
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
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

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')

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

    
    context= {'form':form}        
    return render(request, 'account/perfil.html',context)

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
def productos(request):
    productos = Producto.objects.all()
    subcategorias = Subcategoria.objects.all()

    myFilter = ProductoFilter(request.GET, queryset=productos)
    productos = myFilter.qs

    return render(request,'cruds/tabla-productos.html', {'productos': productos, 'subcategorias': subcategorias, 'myFilter':myFilter})

def categorias(request):
    categorias = Categoria.objects.all()

    myFilter = CategoriaFilter(request.GET, queryset=categorias)
    categorias = myFilter.qs

    return render(request,'cruds/tabla-categorias.html', {'categorias': categorias, 'myFilter':myFilter})

def subcategorias(request):
    subcategorias = Subcategoria.objects.all()

    myFilter = SubcategoriaFilter(request.GET, queryset=subcategorias)
    subcategorias = myFilter.qs

    return render(request,'cruds/tabla-subcategorias.html', {'subcategorias': subcategorias, 'myFilter':myFilter})

def proveedores(request):
    proveedores = Proveedor.objects.all()

    myFilter = ProveedorFilter(request.GET, queryset=proveedores)
    proveedores = myFilter.qs

    return render(request,'cruds/tabla-proveedores.html', {'proveedores': proveedores, 'myFilter':myFilter})

def ordenes(request):
    ordenes = Ordencompra.objects.all()
    return render(request,'cruds/tabla-ordenes.html', {'ordenes': ordenes})
    
def usuarios(request):
    usuarios = User.objects.filter(is_staff=True)
    #empleados = User.objects.filter(groups__name='empleado')

    myFilter = UserFilter(request.GET, queryset=usuarios)
    usuarios = myFilter.qs

    return render(request,'cruds/tabla-usuarios.html', {'usuarios': usuarios, 'myFilter':myFilter})

#crud categoria
def crearCategoria(request):
    form = CategoriaForm()
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias')

    context = {'form':form}
    return render(request,'cruds/categoria.html',context)

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

def eliminarCategoria(request, pk):
    categoria = Categoria.objects.get(idcategoria=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categorias')
        
    context = {'item':categoria}
    return render(request,'cruds/eliminar_categoria.html',context)

#crud subcategoria
def crearSubcategoria(request):
    form = SubcategoriaForm()
    if request.method == 'POST':
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subcategorias')

    context = {'form':form}
    return render(request,'cruds/subcategoria.html',context)

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

def eliminarSubcategoria(request, pk):
    subcategoria = Subcategoria.objects.get(idsubcategoria=pk)
    if request.method == 'POST':
        subcategoria.delete()
        return redirect('subcategorias')
        
    context = {'item':subcategoria}
    return render(request,'cruds/eliminar-subcategoria.html',context)

#crud usuario
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

            u.save()

            au = AuthUser.objects.get(username=username)

            usuario = Usuario(correo=u.email,user=au)
            usuario.save()

            return redirect('usuarios')

    context = {'form':form,'empleado':empleado,'vendedor':vendedor,'administrador':administrador}
    return render(request,'cruds/usuario.html',context)

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
                
            u.save()

            form.save()
            return redirect('usuarios')

    context = {'form':form,'empleado':empleado,'vendedor':vendedor,'administrador':administrador}
    return render(request,'cruds/usuario.html',context)

def eliminarUsuario(request, pk):
    usuario = User.objects.get(id=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuarios')
        
    context = {'item':usuario}
    return render(request,'cruds/eliminar-usuario.html',context)

#crud proveedores
def crearProveedor(request):
    form = ProveedorForm()
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedores')

    context = {'form':form}
    return render(request,'cruds/proveedor.html',context)

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

def eliminarProveedor(request, pk):
    proveedor = Proveedor.objects.get(idproveedor=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedores')
        
    context = {'item':proveedor}
    return render(request,'cruds/eliminar-proveedor.html',context)

#crud Producto
def crearProducto(request):
    form = ProductoForm()
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos')

    context = {'form':form}
    return render(request,'cruds/producto.html',context)

def modificarProducto(request, pk):
    producto = Producto.objects.get(idproducto=pk)
    form = ProductoForm(instance=producto)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos')

    context = {'form':form}
    return render(request,'cruds/producto.html',context)

def eliminarProducto(request, pk):
    producto = Producto.objects.get(idproducto=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos')
        
    context = {'item':producto}
    return render(request,'cruds/eliminar-producto.html',context)


def carro(request):
    return render(request, 'carro.html')

def ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas.html', {'ventas': ventas})

def dashboard(request):
    num_visits=request.session.get('num_visits',0)
    num_visits=request.session['num_visits']=num_visits+1
    context={'num_visits':num_visits,}
    return render(request, 'dashboard.html', context)