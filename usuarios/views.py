from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import grupos_usuarios, grupos_grupos  # <-- Importamos ambos modelos

# Vista principal que lee ambas tablas de PostgreSQL
def listausuarios(request):
    consultagrupos = grupos_usuarios.objects.all() 
    listadogrupos = grupos_grupos.objects.all()  # <-- Traemos todos los grupos reales de la BD
    
    return render(request, 'usuarios/usuarios.html', {
        'consultagrupos': consultagrupos,
        'listadogrupos': listadogrupos  # <-- Los mandamos al HTML
    })

# Guardar Usuario en la BD
def createusuarios(request):
    nvousuario = grupos_usuarios(
        nombre=request.POST['nombre'],
        usuario=request.POST['usuario'],
        passwd=request.POST['passwd'],
        correo=request.POST['correo'],
        grupo_id=request.POST['grupo']
    )
    nvousuario.save()
    return redirect('/pageusuarios')

def creategrupos(request):
    from datetime import date
    
    # Buscamos el ID más alto actual en la base de datos
    ultimo_grupo = grupos_grupos.objects.order_by('-id').first()
    nuevo_id = (ultimo_grupo.id + 1) if ultimo_grupo else 1 # Le sumamos 1 automáticamente

    nvogrupo = grupos_grupos(
        id=nuevo_id,  # <-- Forzamos el ID correlativo automático de manera manual
        nombre=request.POST['nombre_grupo'],
        descripcion=request.POST['descripcion'],
        fecha_creacion=date.today(),
        estatus=True
    )
    nvogrupo.save()
    return redirect('/pageusuarios')