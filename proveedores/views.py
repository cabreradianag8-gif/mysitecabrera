from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Proveedores

def pageproveedores(request, pk_editar=None):
    # --- FORMULARIO DE EDICIÓN ---
    proveedor_a_editar = None
    if pk_editar:
        proveedor_a_editar = get_object_or_404(Proveedores, pk=pk_editar)

    # --- PROVEEDORES ACTIVOS ---
    query = request.GET.get('q', '')
    if query:
        consultaproveedores = Proveedores.objects.filter(
            nombre__icontains=query, estatus=True
        ).order_by('-id') | Proveedores.objects.filter(
            categoria__icontains=query, estatus=True
        ).order_by('-id')
    else:
        consultaproveedores = Proveedores.objects.filter(estatus=True).order_by('-id')
    
    paginator = Paginator(consultaproveedores, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # --- PROVEEDORES INACTIVOS ---
    query_inactivo = request.GET.get('q_inactivo', '')
    if query_inactivo:
        proveedores_inactivos = Proveedores.objects.filter(
            nombre__icontains=query_inactivo, estatus=False
        ).order_by('-id') | Proveedores.objects.filter(
            categoria__icontains=query_inactivo, estatus=False
        ).order_by('-id')
    else:
        proveedores_inactivos = Proveedores.objects.filter(estatus=False).order_by('-id')
        
    paginator_inactivo = Paginator(proveedores_inactivos, 5)
    page_number_inactivo = request.GET.get('page_inactivo')
    page_obj_inactivo = paginator_inactivo.get_page(page_number_inactivo)
    
    context = {
        'consultaproveedores': page_obj,
        'query': query,
        'proveedores_inactivos': page_obj_inactivo,
        'query_inactivo': query_inactivo,
        'proveedor_a_editar': proveedor_a_editar
    }
    return render(request, 'proveedores/proveedores.html', context)


def nuevo_proveedor(request):
    if request.method == 'POST':
        Proveedores.objects.create(
            nombre=request.POST.get('nombre'),
            direccion=request.POST.get('direccion'),
            telefono=request.POST.get('telefono'),
            email=request.POST.get('email'),
            categoria=request.POST.get('categoria')
        )
    return redirect('pageproveedores')


def actualizar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedores, pk=pk)
    if request.method == 'POST':
        proveedor.nombre = request.POST.get('nombre')
        proveedor.direccion = request.POST.get('direccion')
        proveedor.telefono = request.POST.get('telefono')
        proveedor.email = request.POST.get('email')
        proveedor.categoria = request.POST.get('categoria')
        proveedor.save()
    return redirect('pageproveedores')


def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedores, pk=pk)
    proveedor.estatus = False
    proveedor.save()
    return redirect('pageproveedores')


def reactivar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedores, pk=pk)
    proveedor.estatus = True
    proveedor.save()
    return redirect('pageproveedores')