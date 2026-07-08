from django.shortcuts import render, redirect
from .models import Compras
from proveedores.models import Proveedores
from productos.models import Producto
from datetime import datetime

def listacompras(request):
    consultacompras = Compras.objects.all()
    proveedores = Proveedores.objects.all()
    productos = Producto.objects.all()
    
    folio_automatico = datetime.now().strftime("COM-%Y%m%d-%H%M%S")
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    
    return render(request, 'compras/compras.html', {
        'consultacompras': consultacompras,
        'proveedores': proveedores,
        'productos': productos,
        'folio_automatico': folio_automatico,
        'fecha_actual': fecha_actual
    })

def createcompras(request):
    if request.method == 'POST':
        # 1. Creamos la compra principal con los totales monetarios de la adquisición
        nvacompra = Compras(
            folio=request.POST['folio'],
            fecha=request.POST['fecha'],
            subtotal=float(request.POST['subtotal']),
            iva=float(request.POST['iva']),
            total=float(request.POST['total'])
        )
        nvacompra.save()
        
        # 2. Guardamos la relación con los proveedores
        proveedores_ids = request.POST.getlist('proveedor')
        if proveedores_ids:
            nvacompra.proveedor.set(proveedores_ids)
            
        # 3. Procesamos los productos seleccionados y AUMENTAMOS SU STOCK
        productos_ids = request.POST.getlist('producto')
        for prod_id in productos_ids:
            producto_obj = Producto.objects.get(id=prod_id)
            
            # LEER CANTIDAD: Buscamos el campo 'cantidad_X' enviado desde el HTML
            cantidad_comprada = int(request.POST.get(f'cantidad_{prod_id}', 1))
            
            # Guardamos la relación ManyToMany nativa de Django
            nvacompra.producto.add(producto_obj)
            
            # AFECTACIÓN DIRECTA DEL STOCK: Sumamos las unidades al almacén
            producto_obj.stock += cantidad_comprada
            producto_obj.save()
            
    return redirect('/pagecompras')