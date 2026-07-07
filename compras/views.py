from django.shortcuts import render, redirect
from .models import Compras
from proveedores.models import Proveedores  # Ajusta según el nombre real de tu app de proveedores
from productos.models import Producto      # Tu modelo real con 'precio' y 'stock'
from datetime import datetime

def listacompras(request):
    consultacompras = Compras.objects.all().order_by('-id')
    listadoproveedores = Proveedores.objects.all()
    listadoproductos = Producto.objects.all()
    
    return render(request, 'compras/compras.html', {
        'consultacompras': consultacompras,
        'listadoproveedores': listadoproveedores,
        'listadoproductos': listadoproductos
    })

def createcompras(request):
    if request.method == 'POST':
        id_proveedor = request.POST['proveedor']
        
        # 1. Creamos la compra base con valores en 0.00 de forma temporal
        nvacompra = Compras.objects.create(
            folio="TEMP",
            subtotal=0.00,
            iva=0.00,
            total=0.00,
            proveedor_id=id_proveedor
        )
        
        # 2. Asignamos un Folio Único Automático de Compra
        fecha_str = datetime.now().strftime("%Y%m%d")
        nvacompra.folio = f"C-{fecha_str}-{nvacompra.id}"
        
        # 3. Recibimos los arreglos dinámicos del HTML
        productos_ids = request.POST.getlist('productos_seleccionados[]')
        cantidades = request.POST.getlist('cantidades[]')
        
        v_subtotal = 0
        
        # 4. Iterar sobre los productos agregados
        for i in range(len(productos_ids)):
            prod_obj = Producto.objects.get(id=productos_ids[i])
            cant = int(cantidades[i])
            
            # Vinculamos el producto a la relación Muchos a Muchos de la compra
            nvacompra.productos.add(prod_obj)
            
            # Calculamos el costo acumulado usando el precio del producto
            v_subtotal += (prod_obj.precio * cant)
            
            # --- AQUÍ SUMAMOS AL STOCK (ENTRADA DE MERCANCÍA) ---
            prod_obj.stock += cant
            prod_obj.save()
            
        # 5. Cálculos automáticos financieros finales (IVA del 16%)
        v_iva = v_subtotal * 0.16
        v_total = v_subtotal + v_iva
        
        # Guardamos los montos reales calculados por el sistema
        nvacompra.subtotal = v_subtotal
        nvacompra.iva = v_iva
        nvacompra.total = v_total
        nvacompra.save()
        
        return redirect('/pagecompras/')