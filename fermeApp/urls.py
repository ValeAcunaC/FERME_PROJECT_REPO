from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views 
 
urlpatterns = [ 
    path('', views.index, name='index'),
    path('detalle_producto/<int:pk>/', views.detalleProducto, name='detalle_producto'),
    path('ventas', views.ventas, name='ventas'),
    path('dashboard', views.dashboard, name='dashboard'),

    #page info
    path('contacto', views.contacto, name='contacto'),
    path('faq', views.faq, name='faq'),
    path('terminosycondiciones', views.terminosycondiciones, name='terminosycondiciones'),
    path('nosotros', views.nosotros, name='nosotros'),

    #account
    path('login', views.loginPage, name='login'),
    path('register', views.registerPage, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('perfil/<int:pk>/', views.perfil, name='perfil'),
    path('miscompras', views.miscompras, name='miscompras'),
    path('recuperar_contraseña', auth_views.PasswordResetView.as_view(template_name="account/recuperar_contrasena.html"), name='reset_password'),
    path('recuperar_contraseña_enviado', auth_views.PasswordResetDoneView.as_view(template_name="account/recuperar_contrasena_enviado.html"), name='password_reset_done'),
    path('recuperar_contraseña/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/recuperar_contrasena_form.html"), name='password_reset_confirm'),
    path('recuperar_contraseña_exito', auth_views.PasswordResetCompleteView.as_view(template_name="account/recuperar_contrasena_exito.html"), name='password_reset_complete'),

    #shop
    path('carro', views.carro, name='carro'),
    

    #mantenedores
    path('productos', views.productos, name='productos'),
    path('categorias', views.categorias, name='categorias'),
    path('subcategorias', views.subcategorias, name='subcategorias'),
    path('proveedores', views.proveedores, name='proveedores'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('ordenes', views.ordenes, name='ordenes'),

    path('crear_categoria', views.crearCategoria, name='crear_categoria'),
    path('modificar_categoria/<int:pk>/', views.modificarCategoria, name='modificar_categoria'),
    path('eliminar_categoria/<int:pk>/', views.eliminarCategoria, name='eliminar_categoria'),

    path('crear_subcategoria', views.crearSubcategoria, name='crear_subcategoria'),
    path('modificar_subcategoria/<int:pk>/', views.modificarSubcategoria, name='modificar_subcategoria'),
    path('eliminar_subcategoria/<int:pk>/', views.eliminarSubcategoria, name='eliminar_subcategoria'),

    path('crear_proveedor', views.crearProveedor, name='crear_proveedor'),
    path('modificar_proveedor/<int:pk>/', views.modificarProveedor, name='modificar_proveedor'),
    path('eliminar_proveedor/<int:pk>/', views.eliminarProveedor, name='eliminar_proveedor'),

    path('crear_producto', views.crearProducto, name='crear_producto'),
    path('modificar_producto/<int:pk>/', views.modificarProducto, name='modificar_producto'),
    path('eliminar_producto/<int:pk>/', views.eliminarProducto, name='eliminar_producto'),

    path('crear_usuario', views.crearUsuario, name='crear_usuario'),
    path('modificar_usuario/<int:pk>/', views.modificarUsuario, name='modificar_usuario'),
    path('eliminar_usuario/<int:pk>/', views.eliminarUsuario, name='eliminar_usuario'),
    
    
    
] 