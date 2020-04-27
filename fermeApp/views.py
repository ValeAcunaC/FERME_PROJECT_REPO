from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, UsuarioForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import *

def index(request):
    productos = Producto.objects.all()
    subcategorias = Subcategoria.objects.all()
    return render(request,'index.html', {'productos': productos, 'subcategorias': subcategorias})

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
    return render(request,'login.html', context)

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
    return render(request,'register.html',context)

def perfil(request, pk):
    user = User.objects.get(id=pk)

    u = request.user.id
    if u != pk:
        return redirect('index')

    usuario = Usuario.objects.get(user_id=u)

    form = UsuarioForm(instance=usuario)
    #context= {'form':form}
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()

    
    context= {'form':form}        
    return render(request, 'perfil.html',context)

def producto(request):
    # rubro = Rubro.objects.get(idrubro=3)
    # newProveedor = Proveedor(rutproveedor='7-8',nombreproveedor='proveedor3',telefono=123456789,correo='proveedor3@correo.cl',idrubro=rubro)
    # newProveedor.save()
    return render(request,'producto.html')


