from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import models

from .models import Inventario
from productos.models import Producto
from sucursal.models import Sucursal

def pageinventarios(request, pk_editar=None):
    inventario_a_editar = None
    if pk_editar:
        inventario_a_editar = get_object_or_404(Inventario, pk=pk_editar)

    query = request.GET.get('q', '')
    sucursal_id = request.GET.get('sucursal', '')
    
    # Detectar si el usuario quiere ver la papelera (?ver=papelera)
    ver_seccion = request.GET.get('ver', 'activos') 
    
    if ver_seccion == 'papelera':
        registros = Inventario.objects.filter(estatus=False).order_by('-id')
    else:
        registros = Inventario.objects.filter(estatus=True).order_by('-id')
    
    # --- FILTROS Y BÚSQUEDA ---
    if query:
        registros = registros.filter(
            producto__nombre__icontains=query
        ) | registros.filter(
            producto__categoria__icontains=query
        )
        
    if sucursal_id:
        registros = registros.filter(sucursal_id=sucursal_id)

    # --- METRICAS PARA EL DASHBOARD ---
    total_articulos = registros.count()
    alertas_stock = registros.filter(cantidad__lte=models.F('stock_minimo')).count()

    # --- PAGINACIÓN ---
    paginator = Paginator(registros, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    productos_disponibles = Producto.objects.filter(estatus=True) 
    sucursales_disponibles = Sucursal.objects.filter(status=True)

    context = {
        'inventarios': page_obj,
        'query': query,
        'sucursal_seleccionada': sucursal_id,
        'inventario_a_editar': inventario_a_editar,
        'productos_disponibles': productos_disponibles,
        'sucursales_disponibles': sucursales_disponibles,
        'total_articulos': total_articulos,
        'alertas_stock': alertas_stock,
        'ver_seccion': ver_seccion
    }
    return render(request, 'inventarios/inventario.html', context)


def nuevo_inventario(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        sucursal_id = request.POST.get('sucursal')
        cantidad = request.POST.get('cantidad')
        stock_minimo = request.POST.get('stock_minimo')

        inv_existente = Inventario.objects.filter(producto_id=producto_id, sucursal_id=sucursal_id).first()
        
        if inv_existente:
            if not inv_existente.estatus:
                inv_existente.cantidad = cantidad
                inv_existente.stock_minimo = stock_minimo
                inv_existente.estatus = True
                inv_existente.save()
                messages.success(request, f"Se recuperó '{inv_existente.producto.nombre}' de la papelera con stock actualizado.")
            else:
                messages.error(request, "Este producto ya tiene existencias asignadas en esta sucursal.")
        else:
            Inventario.objects.create(
                producto_id=producto_id,
                sucursal_id=sucursal_id,
                cantidad=cantidad,
                stock_minimo=stock_minimo
            )
            messages.success(request, "Inventario asignado correctamente.")
            
    return redirect('rutapageinventarios')


def actualizar_inventario(request, pk):
    item = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        item.cantidad = request.POST.get('cantidad')
        item.stock_minimo = request.POST.get('stock_minimo')
        item.save()
        messages.success(request, f"Existencias de '{item.producto.nombre}' actualizadas.")
    return redirect('rutapageinventarios')


def eliminar_inventario(request, pk):
    item = get_object_or_404(Inventario, pk=pk)
    nombre_prod = item.producto.nombre
    item.estatus = False
    item.save()
    messages.warning(request, f"'{nombre_prod}' fue enviado a la papelera de reciclaje.")
    return redirect('rutapageinventarios')


def restaurar_inventario(request, pk):
    item = get_object_or_404(Inventario, pk=pk)
    item.estatus = True
    item.save()
    messages.success(request, f"'{item.producto.nombre}' ha sido restaurado con éxito.")
    return redirect('rutapageinventarios')