from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Ventas, DetalleVenta
from clientes.models import Cliente
from productos.models import Producto
from sucursal.models import Sucursal
from inventarios.models import Inventario 

def seleccionar_sucursal_view(request):
    """
    Pantalla previa obligatoria para fijar la sucursal de trabajo en la sesión.
    """
    if request.method == 'POST':
        sucursal_id = request.POST.get('sucursal_id')
        if sucursal_id:
            request.session['sucursal_trabajo_id'] = sucursal_id
            return redirect('rutapageventas')
            
    sucursales = Sucursal.objects.filter(status=True)
    return render(request, 'ventas/seleccionar_sucursal.html', {'sucursales': sucursales})


def modulo_ventas_view(request):
    # Si no ha seleccionado sucursal, la mandamos a elegir una
    sucursal_id = request.session.get('sucursal_trabajo_id')
    if not sucursal_id:
        return redirect('seleccionar_sucursal')
        
    sucursal_actual = get_object_or_404(Sucursal, id=sucursal_id)
    lista_clientes = Cliente.objects.filter(estatus=True).order_by('id')
    
    # Traemos los inventarios de esta sucursal que tengan stock > 0
    inventarios_sucursal = Inventario.objects.filter(
        sucursal=sucursal_actual, 
        cantidad__gt=0, 
        producto__estatus=True
    ).select_related('producto').order_by('producto__nombre')
    
    # Generador automático de folios 
    ultima_venta = Ventas.objects.all().order_by('id').last()
    siguiente_id = (ultima_venta.id + 1) if ultima_venta else 1
    proximo_folio = f"VTA-{siguiente_id:04d}"
    
    # Búsqueda por Folio o filtro por sucursal
    query = request.GET.get('buscar_folio', '').strip()
    if query:
        historial_queryset = Ventas.objects.filter(folio__icontains=query, sucursal=sucursal_actual)
    else:
        historial_queryset = Ventas.objects.filter(sucursal=sucursal_actual)
        
    historial_queryset = historial_queryset.prefetch_related('detalleventa_set__producto').order_by('-id')
    
    paginator = Paginator(historial_queryset, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'lista_clientes': lista_clientes,
        'inventarios_sucursal': inventarios_sucursal, # Pasamos los productos con su stock real aquí
        'proximo_folio': proximo_folio,
        'page_obj': page_obj,
        'query': query,
        'sucursal_actual': sucursal_actual
    }
    return render(request, 'ventas/ventas.html', context)


def nueva_venta(request):
    sucursal_id = request.session.get('sucursal_trabajo_id')
    if not sucursal_id:
        return redirect('seleccionar_sucursal')

    if request.method == 'POST':
        sucursal_instancia = get_object_or_404(Sucursal, id=sucursal_id)
        
        try:
            with transaction.atomic():
                cliente_id = request.POST.get('cliente_id')
                producto_ids = request.POST.getlist('producto_ids')
                cantidades = request.POST.getlist('cantidades_prod')
                
                if producto_ids and cantidades and len(producto_ids) == len(cantidades):
                    total_calculado = 0
                    for i in range(len(producto_ids)):
                        prod = get_object_or_404(Producto, id=producto_ids[i])
                        total_calculado += (prod.precio * int(cantidades[i]))
                    
                    ultima_venta = Ventas.objects.all().order_by('id').last()
                    siguiente_id = (ultima_venta.id + 1) if ultima_venta else 1
                    folio_automatico = f"VTA-{siguiente_id:04d}"
                    
                    cliente_instancia = get_object_or_404(Cliente, id=cliente_id)
                    
                    # Guardamos la venta asociando la sucursal activa de la sesión
                    venta = Ventas.objects.create(
                        folio=folio_automatico,
                        total=total_calculado,
                        cliente=cliente_instancia,
                        sucursal=sucursal_instancia,
                        estatus='Completada'
                    )
                    
                    for i in range(len(producto_ids)):
                        prod_instancia = get_object_or_404(Producto, id=producto_ids[i])
                        cant = int(cantidades[i])
                        
                        # Buscamos el registro en la tabla Inventario de esta sucursal
                        inv_producto = Inventario.objects.filter(producto=prod_instancia, sucursal=sucursal_instancia).first()
                        
                        if inv_producto and inv_producto.cantidad >= cant:
                            DetalleVenta.objects.create(
                                venta=venta,
                                producto=prod_instancia,
                                cantidad=cant
                            )
                            # Descontamos del inventario  de la sucursal
                            inv_producto.cantidad -= cant
                            inv_producto.save()
                        else:
                            raise ValueError(f"Stock insuficiente para {prod_instancia.nombre} en esta sucursal.")
                            
                    messages.success(request, f"Venta {folio_automatico} procesada con éxito.")
        except Exception as e:
            messages.error(request, f"Error al procesar: {str(e)}")
                        
    return redirect('rutapageventas')


def cancelar_venta(request, pk):
    venta = get_object_or_404(Ventas, pk=pk)
    if venta.estatus == 'Completada':
        with transaction.atomic():
            venta.estatus = 'Cancelada'
            venta.save()
            
            # Devolver las unidades de forma íntegra AL INVENTARIO DE LA SUCURSAL donde se vendió
            detalles = DetalleVenta.objects.filter(venta=venta)
            for item in detalles:
                inv_producto = Inventario.objects.filter(producto=item.producto, sucursal=venta.sucursal).first()
                if inv_producto:
                    inv_producto.cantidad += item.cantidad
                    inv_producto.save()
                    
            messages.info(request, f"Venta {venta.folio} devuelta al almacén correctamente.")
                
    return redirect('rutapageventas')


def cambiar_sucursal_sesion(request):
    """Ruta rápida por si la cajera quiere cambiar de sucursal sin desloguearse"""
    if 'sucursal_trabajo_id' in request.session:
        del request.session['sucursal_trabajo_id']
    return redirect('seleccionar_sucursal')