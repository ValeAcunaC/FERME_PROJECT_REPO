from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            groups = None

            if request.user.groups.exists():
                groups = request.user.groups.all()
            for g in groups:
                if g.name in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse('No tienes los permisos para acceder a esta página')
        return wrapper_func
    return decorator