from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from django.db import transaction
from .models import Compras, DetalleCompra
from proveedores.models import Proveedores
from productos.models import Producto

def pagecompras_view(request, pk_editar=None):
    compra_a_editar = None
    if pk_editar:
        compra_a_editar = get_object_or_404(Compras, pk=pk_editar)

    lista_proveedores = Proveedores.objects.all().order_by('id')
    lista_productos = Producto.objects.all().order_by('nombre')

    ultima_compra = Compras.objects.all().order_by('id').last()
    siguiente_id = (ultima_compra.id + 1) if ultima_compra else 1
    proximo_folio = f"CMP-{siguiente_id:04d}"

    query = request.GET.get('q', '')
    if query:
        consultacompras = Compras.objects.filter(folio__icontains=query).order_by('-id')
    else:
        # Usamos prefetch_related para obtener eficientemente los detalles y productos
        consultacompras = Compras.objects.all().prefetch_related('detallecompra_set__producto').order_by('-id')
    
    paginator = Paginator(consultacompras, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'consultacompras': page_obj,
        'query': query,
        'compra_a_editar': compra_a_editar,
        'proximo_folio': proximo_folio,
        'fecha_actual': timezone.now().date(),
        'lista_proveedores': lista_proveedores,
        'lista_productos': lista_productos,
    }
    return render(request, 'compras/compras.html', context)


def nueva_compra(request):
    if request.method == 'POST':
        with transaction.atomic():
            # Obtener datos base
            subtotal = float(request.POST.get('subtotal', '0'))
            iva_calculado = subtotal * 0.16
            total_calculado = subtotal + iva_calculado
            
            # Crear la cabecera de la compra
            ultima_compra = Compras.objects.all().order_by('id').last()
            siguiente_id = (ultima_compra.id + 1) if ultima_compra else 1
            folio_automatico = f"CMP-{siguiente_id:04d}"
            
            compra = Compras.objects.create(
                folio=folio_automatico,
                fecha=timezone.now().date(),
                subtotal=subtotal,
                iva=iva_calculado,
                total=total_calculado,
                estatus='Procesada'
            )
            
            # Asignar proveedores
            compra.proveedor.set(request.POST.getlist('proveedor_ids'))
            
            # Recuperar arrays
            producto_ids = request.POST.getlist('producto_ids')
            costos = request.POST.getlist('costos_prod')
            cantidades = request.POST.getlist('cantidades_prod')
            
            # VALIDACIÓN DE SEGURIDAD: Solo procesar si las listas tienen el mismo largo
            if len(producto_ids) == len(costos) == len(cantidades):
                for i in range(len(producto_ids)):
                    prod_id = producto_ids[i]
                    costo_un = float(costos[i])
                    cant = int(cantidades[i])
                    
                    prod_instancia = get_object_or_404(Producto, id=prod_id)
                    
                    # Guardar detalle
                    DetalleCompra.objects.create(
                        compra=compra,
                        producto=prod_instancia,
                        cantidad=cant,
                        costo_compra=costo_un
                    )
                    
                    # Afectar stock
                    prod_instancia.stock += cant
                    prod_instancia.save()
            else:
                # Si falló la sincronización, cancelamos la creación para evitar basura
                compra.delete()
                
    return redirect('rutapagecompras')


def cancelar_compra(request, pk):
    # Lógica de protección financiera e inventario
    compra = get_object_or_404(Compras, pk=pk)
    
    if compra.estatus == 'Procesada':
        with transaction.atomic():
            compra.estatus = 'Cancelada'
            compra.save()
            
            # Revertir el Stock: Restar las unidades agregadas previamente
            detalles = DetalleCompra.objects.filter(compra=compra)
            for item in detalles:
                producto = item.producto
                producto.stock -= item.cantidad
                producto.save()
                
    return redirect('rutapagecompras')