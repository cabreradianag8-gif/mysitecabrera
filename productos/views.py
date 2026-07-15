from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Producto

def pageproductos(request, pk_editar=None):
    # --- FORMULARIO DE EDICIÓN ---
    producto_a_editar = None
    if pk_editar:
        producto_a_editar = get_object_or_404(Producto, pk=pk_editar)

    # --- PRODUCTOS ACTIVOS ---
    query = request.GET.get('q', '')
    if query:
        consultaproductos = Producto.objects.filter(
            nombre__icontains=query, estatus=True
        ).order_by('-id') | Producto.objects.filter(
            categoria__icontains=query, estatus=True
        ).order_by('-id')
    else:
        consultaproductos = Producto.objects.filter(estatus=True).order_by('-id')
    
    paginator = Paginator(consultaproductos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # --- PRODUCTOS INACTIVOS ---
    query_inactivo = request.GET.get('q_inactivo', '')
    if query_inactivo:
        productos_inactivos = Producto.objects.filter(
            nombre__icontains=query_inactivo, estatus=False
        ).order_by('-id') | Producto.objects.filter(
            categoria__icontains=query_inactivo, estatus=False
        ).order_by('-id')
    else:
        productos_inactivos = Producto.objects.filter(estatus=False).order_by('-id')
        
    paginator_inactivo = Paginator(productos_inactivos, 5)
    page_number_inactivo = request.GET.get('page_inactivo')
    page_obj_inactivo = paginator_inactivo.get_page(page_number_inactivo)
    
    context = {
        'consultaproductos': page_obj,
        'query': query,
        'productos_inactivos': page_obj_inactivo,
        'query_inactivo': query_inactivo,
        'producto_a_editar': producto_a_editar
    }
    return render(request, 'productos/productos.html', context)


def nuevo_producto(request):
    if request.method == 'POST':
        Producto.objects.create(
            nombre=request.POST.get('nombre'),
            precio=request.POST.get('precio'),
            descripcion=request.POST.get('descripcion'),
            categoria=request.POST.get('categoria')
        )
    return redirect('rutapageproductos')


def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.precio = request.POST.get('precio')
        producto.descripcion = request.POST.get('descripcion')
        producto.categoria = request.POST.get('categoria')
        producto.save()
    return redirect('rutapageproductos')


def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.estatus = False
    producto.save()
    return redirect('rutapageproductos')


def reactivar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.estatus = True
    producto.save()
    return redirect('rutapageproductos')