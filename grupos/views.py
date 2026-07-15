from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import grupos_grupos
import datetime

# 1. CONSULTAR Y LISTAR 
def pagegrupos(request):
    query = request.GET.get('buscar_nombre', '')
    if query:
        lista_grupos = grupos_grupos.objects.filter(nombre__icontains=query).order_by('-id')
    else:
        lista_grupos = grupos_grupos.objects.all().order_by('-id')

    paginator = Paginator(lista_grupos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #  detectar si se está EDITANDO un grupo
    editar_id = request.GET.get('editar', None)
    grupo_a_editar = None
    if editar_id:
        grupo_a_editar = get_object_or_404(grupos_grupos, id=editar_id)

    context = {
        'page_obj': page_obj,
        'query': query,
        'grupo_a_editar': grupo_a_editar, 
        'fecha_hoy': datetime.date.today().strftime('%Y-%m-%d')
    }
    return render(request, 'grupos/grupos.html', context)

# 2. CREAR
def nuevo_grupo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha_creacion = request.POST.get('fecha_creacion')
        
        grupos_grupos.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            fecha_creacion=fecha_creacion,
            estatus=True
        )
        messages.success(request, "¡Grupo de permisos creado exitosamente!")
        return redirect('rutapagegrupos')

# 3. ACTUALIZAR
def actualizar_grupo(request, grupo_id):
    if request.method == 'POST':
        grupo = get_object_or_404(grupos_grupos, id=grupo_id)
        grupo.nombre = request.POST.get('nombre')
        grupo.descripcion = request.POST.get('descripcion')
        grupo.fecha_creacion = request.POST.get('fecha_creacion')
        grupo.save()
        
        messages.success(request, f"¡Grupo '{grupo.nombre}' actualizado correctamente!")
        return redirect('rutapagegrupos')

# 4. DESACTIVAR / REACTIVAR (Estatus)
def cambiar_estatus_grupo(request, grupo_id):
    grupo = get_object_or_404(grupos_grupos, id=grupo_id)
    grupo.estatus = not grupo.estatus
    grupo.save()
    
    if grupo.estatus:
        messages.success(request, f"El grupo '{grupo.nombre}' ha sido Reactivado.")
    else:
        messages.warning(request, f"El grupo '{grupo.nombre}' ha sido Desactivado.")
        
    return redirect('rutapagegrupos')