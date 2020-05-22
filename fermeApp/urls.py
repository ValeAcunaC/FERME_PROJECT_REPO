from django.urls import path 
from . import views 
 
urlpatterns = [ 
    path('', views.index, name='index'),
    path('producto', views.producto, name='producto'),

    #account
    path('login', views.loginPage, name='login'),
    path('register', views.registerPage, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('perfil/<int:pk>/', views.perfil, name='perfil'),
    path('miscompras', views.miscompras, name='miscompras'),

    #mantenedores
    path('productos', views.productos, name='productos'),
    path('categorias', views.categorias, name='categorias'),
    path('subcategorias', views.subcategorias, name='subcategorias'),
    path('proveedores', views.proveedores, name='proveedores'),
    path('ordenes', views.ordenes, name='ordenes'),
    
    #page info
    path('contacto', views.contacto, name='contacto'),
    path('faq', views.faq, name='faq'),
    path('terminosycondiciones', views.terminosycondiciones, name='terminosycondiciones'),
    path('nosotros', views.nosotros, name='nosotros'),
    
] 