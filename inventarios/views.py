from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Inventario
from productos.models import Producto
from proveedores.models import Proveedores
from sucursal.models import Sucursal

# 1. CONSULTAR Y LISTAR
def pageinventarios(request):
    query = request.GET.get('buscar_inventario', '')
    
    # Filtrar por nombre de producto si existe búsqueda
    if query:
        lista_inventario = Inventario.objects.filter(producto__nombre__icontains=query).order_by('-id')
    else:
        lista_inventario = Inventario.objects.all().order_by('-id')

    # Paginación exigida de 5 en 5
    paginator = Paginator(lista_inventario, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Capturar si se va a editar un registro
    editar_id = request.GET.get('editar', None)
    inventario_a_editar = None
    if editar_id:
        inventario_a_editar = get_object_or_404(Inventario, id=editar_id)

    # Cargar dropdowns relacionales (filtrando solo los activos si tu sistema lo requiere)
    productos_disponibles = Producto.objects.filter(estatus=True)
    proveedores_disponibles = Proveedores.objects.filter(estatus=True)
    sucursales_disponibles = Sucursal.objects.all() # O .filter(status=True) según tu modelo sucursal

    context = {
        'page_obj': page_obj,
        'query': query,
        'inventario_a_editar': inventario_a_editar,
        'productos_disponibles': productos_disponibles,
        'proveedores_disponibles': proveedores_disponibles,
        'sucursales_disponibles': sucursales_disponibles
    }
    return render(request, 'inventarios/inventario.html', context)

# 2. CREAR
def nuevo_inventario(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        proveedor_id = request.POST.get('proveedor')
        sucursal_id = request.POST.get('sucursal')
        stock_local = request.POST.get('stock_local', 0)

        prod_obj = get_object_or_404(Producto, id=producto_id)
        prov_obj = get_object_or_404(Proveedores, id=proveedor_id)
        suc_obj = get_object_or_404(Sucursal, id=sucursal_id)

        # Validar el unique_together antes de insertar para evitar errores de caída del sistema
        existe = Inventario.objects.filter(producto=prod_obj, proveedor=prov_obj, sucursal=suc_obj).exists()
        if existe:
            messages.error(request, f"Error: Ya existe un registro de inventario para {prod_obj.nombre} con este proveedor en esa sucursal.")
            return redirect('rutapageinventarios')

        Inventario.objects.create(
            producto=prod_obj,
            proveedor=prov_obj,
            sucursal=suc_obj,
            stock_local=int(stock_local)
        )
        messages.success(request, "¡Asignación de stock de inventario creada con éxito!")
        return redirect('rutapageinventarios')

# 3. ACTUALIZAR
def actualizar_inventario(request, inventario_id):
    if request.method == 'POST':
        inv_inst = get_object_or_404(Inventario, id=inventario_id)
        producto_id = request.POST.get('producto')
        proveedor_id = request.POST.get('proveedor')
        sucursal_id = request.POST.get('sucursal')
        stock_local = request.POST.get('stock_local')

        prod_obj = get_object_or_404(Producto, id=producto_id)
        prov_obj = get_object_or_404(Proveedores, id=proveedor_id)
        suc_obj = get_object_or_404(Sucursal, id=sucursal_id)

        # Validar si cambiaron llaves y que no choquen con otro registro existente
        if (inv_inst.producto != prod_obj or inv_inst.proveedor != prov_obj or inv_inst.sucursal != suc_obj):
            if Inventario.objects.filter(producto=prod_obj, proveedor=prov_obj, sucursal=suc_obj).exists():
                messages.error(request, "Error: No se pudo actualizar porque esa combinación ya existe.")
                return redirect('rutapageinventarios')

        inv_inst.producto = prod_obj
        inv_inst.proveedor = prov_obj
        inv_inst.sucursal = suc_obj
        inv_inst.stock_local = int(stock_local)
        inv_inst.save()

        messages.success(request, "¡Registro de inventario actualizado correctamente!")
        return redirect('rutapageinventarios')

# 4. ELIMINAR (Para limpiar asignaciones erróneas)
def eliminar_inventario(request, inventario_id):
    inv_inst = get_object_or_404(Inventario, id=inventario_id)
    nombre_prod = inv_inst.producto.nombre
    inv_inst.delete()
    messages.warning(request, f"Se ha removido el control de inventario para '{nombre_prod}'.")
    return redirect('rutapageinventarios')
