from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Sucursal
from empleados.models import empleados
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Sucursal
from empleados.models import empleados

def pagesucursal_view(request, pk_editar=None):
    sucursal_a_editar = None
    empleados_seleccionados_ids = []
    
    if pk_editar:
        sucursal_a_editar = get_object_or_404(Sucursal, pk=pk_editar)
        # Obtenemos los IDs de los empleados ya asignados a esta sucursal
        empleados_seleccionados_ids = sucursal_a_editar.personal.values_list('id', flat=True)

    # Traemos todos los empleados activos para listarlos en el formulario
    todos_los_empleados = empleados.objects.filter(status=True).order_by('nombre')

    # --- 1. BUSCADOR Y LÓGICA DE SUCURSALES ACTIVAS ---
    query = request.GET.get('q', '')
    if query:
        consultasucursales = Sucursal.objects.filter(nombre__icontains=query, status=True).order_by('-id')
    else:
        consultasucursales = Sucursal.objects.filter(status=True).order_by('-id')
    
    paginator = Paginator(consultasucursales, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # --- 2. BUSCADOR Y LÓGICA DE SUCURSALES INACTIVAS 
    query_inactivo = request.GET.get('q_inactivo', '')
    if query_inactivo:
        sucursales_inactivas = Sucursal.objects.filter(nombre__icontains=query_inactivo, status=False).order_by('-id')
    else:
        sucursales_inactivas = Sucursal.objects.filter(status=False).order_by('-id')
    
    context = {
        'consultasucursales': page_obj,
        'query': query,
        'sucursales_inactivas': sucursales_inactivas,
        'query_inactivo': query_inactivo,  # <-- Enviamos la variable limpia al HTML
        'sucursal_a_editar': sucursal_a_editar,
        'todos_los_empleados': todos_los_empleados,
        'empleados_seleccionados_ids': empleados_seleccionados_ids
    }
    return render(request, 'sucursal/sucursal.html', context)


def nueva_sucursal(request):
    if request.method == 'POST':
        nueva = Sucursal.objects.create(
            nombre=request.POST.get('nombre'),
            direccion=request.POST.get('direccion'),
            telefono=request.POST.get('telefono'),
            ciudad=request.POST.get('ciudad')
        )
        # Al ser ManyToMany, obtenemos la lista completa de IDs de empleados seleccionados
        empleados_ids = request.POST.getlist('personal_ids')
        if empleados_ids:
            nueva.personal.set(empleados_ids)
            
    return redirect('rutapagesucursal')


def actualizar_sucursal(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    if request.method == 'POST':
        sucursal.nombre = request.POST.get('nombre')
        sucursal.direccion = request.POST.get('direccion')
        sucursal.telefono = request.POST.get('telefono')
        sucursal.ciudad = request.POST.get('ciudad')
        sucursal.save()
        
        # Sincronizamos la nueva lista de empleados seleccionados
        empleados_ids = request.POST.getlist('personal_ids')
        sucursal.personal.set(empleados_ids)
        
    return redirect('rutapagesucursal')


def eliminar_sucursal(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    sucursal.status = False
    sucursal.save()
    return redirect('rutapagesucursal')


def reactivar_sucursal(request, pk):
    sucursal = get_object_or_404(Sucursal, pk=pk)
    sucursal.status = True
    sucursal.save()
    return redirect('rutapagesucursal')