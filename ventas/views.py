from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.core.paginator import Paginator
from .models import Ventas, DetalleVenta
from clientes.models import Cliente
from productos.models import Producto

def modulo_ventas_view(request):
    lista_clientes = Cliente.objects.all().order_by('id')
    # Solo mostramos en el selector aquellos productos que tengan stock disponible
    lista_productos = Producto.objects.filter(stock__gt=0, estatus=True).order_by('nombre')
    
    # Generador automático de folios (VTA-0001, VTA-0002...)
    ultima_venta = Ventas.objects.all().order_by('id').last()
    siguiente_id = (ultima_venta.id + 1) if ultima_venta else 1
    proximo_folio = f"VTA-{siguiente_id:04d}"
    
    # Búsqueda por Folio Exacto si el usuario lo utiliza en el buscador
    query = request.GET.get('buscar_folio', '').strip()
    if query:
        historial_queryset = Ventas.objects.filter(folio__icontains=query)
    else:
        historial_queryset = Ventas.objects.all()
        
    historial_queryset = historial_queryset.prefetch_related('detalleventa_set__producto').order_by('-id')
    
    # Paginación organizada de 5 registros por página
    paginator = Paginator(historial_queryset, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'lista_clientes': lista_clientes,
        'lista_productos': lista_productos,
        'proximo_folio': proximo_folio,
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'ventas/ventas.html', context)


def nueva_venta(request):
    if request.method == 'POST':
        with transaction.atomic():
            cliente_id = request.POST.get('cliente_id')
            producto_ids = request.POST.getlist('producto_ids')
            cantidades = request.POST.getlist('cantidades_prod')
            
            if producto_ids and cantidades and len(producto_ids) == len(cantidades):
                # 1. Calcular el monto total neto multiplicando por los precios reales del catálogo
                total_calculado = 0
                for i in range(len(producto_ids)):
                    prod = get_object_or_404(Producto, id=producto_ids[i])
                    total_calculado += (prod.precio * int(cantidades[i]))
                
                # 2. Re-generar el folio consecutivo de seguridad en el servidor
                ultima_venta = Ventas.objects.all().order_by('id').last()
                siguiente_id = (ultima_venta.id + 1) if ultima_venta else 1
                folio_automatico = f"VTA-{siguiente_id:04d}"
                
                cliente_instancia = get_object_or_404(Cliente, id=cliente_id)
                
                # 3. Guardar la cabecera del cobro
                venta = Ventas.objects.create(
                    folio=folio_automatico,
                    total=total_calculado,
                    cliente=cliente_instancia,
                    estatus='Completada'
                )
                
                # 4. Registrar los conceptos de la venta y restar stock físico
                for i in range(len(producto_ids)):
                    prod_instancia = get_object_or_404(Producto, id=producto_ids[i])
                    cant = int(cantidades[i])
                    
                    if prod_instancia.stock >= cant:
                        DetalleVenta.objects.create(
                            venta=venta,
                            producto=prod_instancia,
                            cantidad=cant
                        )
                        # Descontar del Stock disponible
                        prod_instancia.stock -= cant
                        prod_instancia.save()
                    else:
                        # Protección por si intentan enviar peticiones truqueadas saltándose el JS
                        raise ValueError(f"Stock insuficiente para {prod_instancia.nombre}")
                        
    return redirect('rutapageventas')


def cancelar_venta(request, pk):
    venta = get_object_or_404(Ventas, pk=pk)
    if venta.estatus == 'Completada':
        with transaction.atomic():
            venta.estatus = 'Cancelada'
            venta.save()
            
            # Devolver de forma íntegra las unidades al stock del inventario
            detalles = DetalleVenta.objects.filter(venta=venta)
            for item in detalles:
                producto = item.producto
                producto.stock += item.cantidad
                producto.save()
                
    return redirect('rutapageventas')