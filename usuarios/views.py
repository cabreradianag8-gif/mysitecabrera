from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import grupos_usuarios
from grupos.models import grupos_grupos
from empleados.models import empleados as EmpleadoModel

# 1. CONSULTAR Y LISTAR
def pageusuarios(request):
    query = request.GET.get('buscar_usuario', '')
    if query:
        lista_usuarios = grupos_usuarios.objects.filter(usuario__icontains=query).order_by('-id')
    else:
        lista_usuarios = grupos_usuarios.objects.all().order_by('-id')

    paginator = Paginator(lista_usuarios, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    editar_id = request.GET.get('editar', None)
    usuario_a_editar = None
    if editar_id:
        usuario_a_editar = get_object_or_404(grupos_usuarios, id=editar_id)

    grupos_disponibles = grupos_grupos.objects.filter(estatus=True)
    empleados_disponibles = EmpleadoModel.objects.filter(status=True)

    context = {
        'page_obj': page_obj,
        'query': query,
        'usuario_a_editar': usuario_a_editar,
        'grupos_disponibles': grupos_disponibles,
        'empleados_disponibles': empleados_disponibles
    }
    return render(request, 'usuarios/usuarios.html', context)

# 2. CREAR
def nuevo_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        usuario = request.POST.get('usuario')
        passwd = request.POST.get('passwd')
        correo = request.POST.get('correo')
        grupo_id = request.POST.get('grupo')
        empleado_id = request.POST.get('empleado')

        grupo_obj = get_object_or_404(grupos_grupos, id=grupo_id)
        empleado_obj = get_object_or_404(EmpleadoModel, id=empleado_id) if empleado_id else None

        grupos_usuarios.objects.create(
            nombre=nombre,
            usuario=usuario,
            passwd=passwd,
            correo=correo,
            grupo=grupo_obj,
            empleado=empleado_obj,
            estatus=True # Se crea activo 
        )
        messages.success(request, f"¡Usuario '{usuario}' registrado exitosamente!")
        return redirect('rutapageusuarios')

# 3. ACTUALIZAR
def actualizar_usuario(request, usuario_id):
    if request.method == 'POST':
        user_inst = get_object_or_404(grupos_usuarios, id=usuario_id)
        grupo_id = request.POST.get('grupo')
        empleado_id = request.POST.get('empleado')

        user_inst.nombre = request.POST.get('nombre')
        user_inst.usuario = request.POST.get('usuario')
        user_inst.passwd = request.POST.get('passwd')
        user_inst.correo = request.POST.get('correo')
        user_inst.grupo = get_object_or_404(grupos_grupos, id=grupo_id)
        user_inst.empleado = get_object_or_404(EmpleadoModel, id=empleado_id) if empleado_id else None
        
        user_inst.save()
        messages.success(request, f"¡Usuario '{user_inst.usuario}' actualizado!")
        return redirect('rutapageusuarios')

# 4. DESACTIVAR / REACTIVAR ESTATUS PROPIO
from django.db.models import F

def cambiar_estatus_usuario(request, usuario_id):
    user_inst = get_object_or_404(grupos_usuarios, id=usuario_id)
    
    nuevo_estado = not user_inst.estatus
    
    grupos_usuarios.objects.filter(id=usuario_id).update(estatus=nuevo_estado)
    
    if nuevo_estado:
        messages.success(request, f"¡El usuario '{user_inst.usuario}' ahora está Activo en la BD!")
    else:
        messages.warning(request, f"¡El usuario '{user_inst.usuario}' ahora está Inactivo en la BD!")
        
    return redirect('rutapageusuarios')