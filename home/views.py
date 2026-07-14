from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from usuarios.models import grupos_usuarios  # Importación de tu modelo exacto

def login_view(request):
    """
    Controla el inicio de sesión validando las credenciales en texto plano
    directamente desde tu tabla personalizada 'grupos_usuarios'.
    """
    if request.method == 'POST':
        user_input = request.POST.get('usuario')
        pass_input = request.POST.get('password')
        
        # 1. Buscamos directamente en tu tabla personalizada (como en tu DBeaver)
        perfil = grupos_usuarios.objects.filter(
            usuario=user_input, 
            passwd=pass_input, 
            estatus=True
        ).first()
        
        if perfil:
            # 2. Sincronización automática con la sesión interna de Django
            User = get_user_model()
            
            # Si el usuario no existe en la tabla interna de Django (auth_user), la creamos al vuelo
            django_user, created = User.objects.get_or_create(username=user_input)
            if created:
                django_user.email = perfil.correo
                django_user.save()
            
            # Iniciamos formalmente la cookie/sesión en el navegador del cliente
            login(request, django_user)
            return redirect('home_index')
        else:
            # Mensaje en caso de error de credenciales
            messages.error(request, "Usuario o contraseña incorrectos.")
            
    return render(request, 'home/login.html')


@login_required
def index(request):
    # Ya no necesitas armar el diccionario 'context' con los roles aquí,
    # el procesador de contexto lo hace por ti en segundo plano.
    return render(request, 'home/index.html')


def logout_view(request):
    """
    Termina de forma segura la sesión actual en el navegador y 
    redirecciona automáticamente a la pantalla de login.
    """
    logout(request)
    return redirect('login')