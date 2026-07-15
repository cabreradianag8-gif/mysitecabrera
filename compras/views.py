from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import transaction
from datetime import datetime
import random

from .models import Compras, DetalleCompra
from proveedores.models import Proveedores
from inventarios.models import Inventario

def pagecompras(request):
    query = request.GET.get('q', '')
    compras_lista = Compras.objects.all().order_by('-id')
    
    if query:
        compras_lista = compras_lista.filter(folio__icontains=query)

    paginator = Paginator(compras_lista, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'compras': page_obj,
        'query': query,
        'inventarios_disponibles': Inventario.objects.all(),
        'proveedores_disponibles': Proveedores.objects.filter(estatus=True),
    }
    return render(request, 'compras/compras.html', context)


def registrar_compra(request):
    if request.method == 'POST':
        proveedores_ids = request.POST.getlist('proveedores')
        
        # Listas dinámicas 
        inventarios_ids = request.POST.getlist('inventarios[]')
        cantidades = request.POST.getlist('cantidades[]')
        costos = request.POST.getlist('costos[]')

        if not inventarios_ids:
            messages.error(request, "Debes añadir al menos un artículo al desglose de la compra.")
            return redirect('rutapagecompras')

        try:
            with transaction.atomic():
                # 1. ASIGNACIÓN AUTOMÁTICA DE FECHA Y FOLIO UNICO
                ahora = datetime.now()
                fecha_automatica = ahora.date()
                # Genera un folio único automático
                folio_automatico = f"COMP-{ahora.strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
                
                # 2. CÁLCULO AUTOMÁTICO DE VALORES MONETARIOS
                calculo_subtotal = 0.0
                for cant, costo in zip(cantidades, costos):
                    calculo_subtotal += int(cant) * float(costo)
                
                calculo_iva = calculo_subtotal * 0.16  
                calculo_total = calculo_subtotal + calculo_iva

                # 3. GUARDAR EN LA BASE DE DATOS 
                nueva_compra = Compras.objects.create(
                    folio=folio_automatico,
                    fecha=fecha_automatica,
                    subtotal=calculo_subtotal,
                    iva=calculo_iva,
                    total=calculo_total,
                    estatus='Procesada'
                )
                
                # Asociar Proveedores ManyToMany
                nueva_compra.proveedor.set(proveedores_ids)
                
                # 4. Registrar detalles y actualizar stock en Inventarios
                for inv_id, cant, costo in zip(inventarios_ids, cantidades, costos):
                    inventario_obj = Inventario.objects.get(id=inv_id)
                    cantidad_unidades = int(cant)
                    
                    DetalleCompra.objects.create(
                        compra=nueva_compra,
                        producto=inventario_obj.producto,
                        inventario=inventario_obj,
                        cantidad=cantidad_unidades,
                        costo_compra=float(costo)
                    )
                    
                    # Sumar las unidades directamente al inventario de esa sucursal
                    inventario_obj.cantidad += cantidad_unidades
                    inventario_obj.save()
                    
                messages.success(request, f"Compra {folio_automatico} procesada automáticamente. ¡Inventarios actualizados!")
                
        except Exception as e:
            messages.error(request, f"Error al procesar la operación automatizada: {str(e)}")
            
    return redirect('rutapagecompras')


def cancelar_compra(request, pk):
    compra = get_object_or_404(Compras, pk=pk)
    if compra.estatus == 'Procesada':
        try:
            with transaction.atomic():
                detalles = DetalleCompra.objects.filter(compra=compra)
                for detalle in detalles:
                    detalle.inventario.cantidad -= detalle.cantidad
                    detalle.inventario.save()
                
                compra.estatus = 'Cancelada'
                compra.save()
                messages.warning(request, f"Compra {compra.folio} cancelada. El stock fue retirado de los almacenes.")
        except Exception as e:
            messages.error(request, f"No se pudo revertir el stock: {str(e)}")
    else:
        messages.error(request, "Esta compra ya se encuentra cancelada.")
    return redirect('rutapagecompras')