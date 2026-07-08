from django.shortcuts import render, redirect
from .models import Ventas
from clientes.models import Cliente
from productos.models import Producto  
from datetime import datetime

def listaventas(request):
    consultaventas = Ventas.objects.all().order_by('-id')
    listadoclientes = Cliente.objects.all()
    listadoproductos = Producto.objects.all() 
    
    return render(request, 'ventas/ventas.html', {
        'consultaventas': consultaventas,
        'listadoclientes': listadoclientes,
        'listadoproductos': listadoproductos
    })

def createventas(request):
    if request.method == 'POST':
        id_cliente = request.POST['cliente']
        cliente_obj = Cliente.objects.get(id=id_cliente)
        
        # 1. Crear registro base de la venta
        nueva_venta = Ventas.objects.create(
            folio="TEMP",
            cliente=cliente_obj,
            total=0.00
        )
        
        # 2. Asignar Folio Automático único
        fecha_str = datetime.now().strftime("%Y%m%d")
        nueva_venta.folio = f"V-{fecha_str}-{nueva_venta.id}"
        
        # 3. Obtener listas enviadas por el formulario
        productos_ids = request.POST.getlist('productos_seleccionados[]')
        cantidades = request.POST.getlist('cantidades[]')
        
        v_total = 0
        
        # 4. Vincular la relación Muchos a Muchos, calcular y BAJAR EL STOCK REAL
        for i in range(len(productos_ids)):
            prod_obj = Producto.objects.get(id=productos_ids[i])
            cant = int(cantidades[i])
            
            # Vinculamos el producto a la venta usando la relación ManyToMany nativa
            nueva_venta.productos.add(prod_obj)
            
            # Sumamos al total usando tu columna real 'precio'
            v_total += (prod_obj.precio * cant)
            

            prod_obj.stock -= cant
            prod_obj.save()
            
        # 5. Guardar el gran total de la venta
        nueva_venta.total = v_total
        nueva_venta.save()
            
        return redirect('/pageventas/')