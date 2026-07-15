from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import empleados

def pageempleados_view(request, pk_editar=None):
    # --- FORMULARIO DE EDICIÓN ---
    empleado_a_editar = None
    if pk_editar:
        empleado_a_editar = get_object_or_404(empleados, pk=pk_editar)

    # --- EMPLEADOS ACTIVOS ---
    query = request.GET.get('q', '')
    if query:
        consultaempleados = empleados.objects.filter(
            nombre__icontains=query, status=True
        ).order_by('-id') | empleados.objects.filter(
            departamento__icontains=query, status=True
        ).order_by('-id')
    else:
        consultaempleados = empleados.objects.filter(status=True).order_by('-id')
    
    paginator = Paginator(consultaempleados, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # --- EMPLEADOS INACTIVOS ---
    query_inactivo = request.GET.get('q_inactivo', '')
    if query_inactivo:
        empleados_inactivos = empleados.objects.filter(
            nombre__icontains=query_inactivo, status=False
        ).order_by('-id') | empleados.objects.filter(
            departamento__icontains=query_inactivo, status=False
        ).order_by('-id')
    else:
        empleados_inactivos = empleados.objects.filter(status=False).order_by('-id')
        
    paginator_inactivo = Paginator(empleados_inactivos, 5)
    page_number_inactivo = request.GET.get('page_inactivo')
    page_obj_inactivo = paginator_inactivo.get_page(page_number_inactivo)
    
    context = {
        'consultaempleados': page_obj,
        'query': query,
        'empleados_inactivos': page_obj_inactivo,
        'query_inactivo': query_inactivo,
        'empleado_a_editar': empleado_a_editar
    }
    return render(request, 'empleados/empleados.html', context)


def nuevo_empleado(request):
    if request.method == 'POST':
        empleados.objects.create(
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            departamento=request.POST.get('departamento'),
            telefono=request.POST.get('telefono'),
            email=request.POST.get('email'),
            turno=request.POST.get('turno')
        )
    return redirect('rutapageempleados')


def actualizar_empleado(request, pk):
    empleado = get_object_or_404(empleados, pk=pk)
    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre')
        empleado.apellido = request.POST.get('apellido')
        empleado.departamento = request.POST.get('departamento')
        empleado.telefono = request.POST.get('telefono')
        empleado.email = request.POST.get('email')
        empleado.turno = request.POST.get('turno')
        empleado.save()
    return redirect('rutapageempleados')


def eliminar_empleado(request, pk):
    empleado = get_object_or_404(empleados, pk=pk)
    empleado.status = False  
    empleado.save()
    return redirect('rutapageempleados')


def reactivar_empleado(request, pk):
    empleado = get_object_or_404(empleados, pk=pk)
    empleado.status = True
    empleado.save()
    return redirect('rutapageempleados')