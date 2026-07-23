from django.shortcuts import render, redirect, get_object_or_404 
from django.core.paginator import Paginator
from .models import Cliente

def pageclientes(request, pk_editar=None):
    # FORMULARIO
    cliente_a_editar = None
    if pk_editar:
        # Si viene un ID en la URL, buscamos al cliente para meterlo al formulario
        cliente_a_editar = get_object_or_404(Cliente, pk=pk_editar)

    # --- CLIENTES ACTIVOS ---
    query = request.GET.get('q', '')
    if query:
        consultaclientes = Cliente.objects.filter(
            nombre__icontains=query, estatus=True
        ).order_by('-id') | Cliente.objects.filter(
            apellido__icontains=query, estatus=True
        ).order_by('-id')
    else:
        consultaclientes = Cliente.objects.filter(estatus=True).order_by('-id')
    
    paginator = Paginator(consultaclientes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # --- CLIENTES INACTIVOS ---
    query_inactivo = request.GET.get('q_inactivo', '')
    if query_inactivo:
        clientes_inactivos = Cliente.objects.filter(
            nombre__icontains=query_inactivo, estatus=False
        ).order_by('-id') | Cliente.objects.filter(
            apellido__icontains=query_inactivo, estatus=False
        ).order_by('-id')
    else:
        clientes_inactivos = Cliente.objects.filter(estatus=False).order_by('-id')
        
    paginator_inactivo = Paginator(clientes_inactivos, 5)
    page_number_inactivo = request.GET.get('page_inactivo')
    page_obj_inactivo = paginator_inactivo.get_page(page_number_inactivo)
    
    context = {
        'consultaclientes': page_obj,
        'query': query,
        'clientes_inactivos': page_obj_inactivo,
        'query_inactivo': query_inactivo,
        'cliente_a_editar': cliente_a_editar  # <-- Pasamos el cliente seleccionado
    }
    return render(request, 'clientes/clientes.html', context)


# Acción POST para actualizar un registro existente
def actualizar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.sexo = request.POST.get('sexo')
        cliente.tipo = request.POST.get('tipo')
        cliente.direccion = request.POST.get('direccion')
        cliente.telefono = request.POST.get('telefono')
        cliente.email = request.POST.get('email')
        cliente.save()
    return redirect('pageclientes')


def nuevo_cliente(request):
    if request.method == 'POST':
        Cliente.objects.create(
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            sexo=request.POST.get('sexo'),
            tipo=request.POST.get('tipo'),
            direccion=request.POST.get('direccion'),
            telefono=request.POST.get('telefono'),
            email=request.POST.get('email')
        )
    return redirect('pageclientes')

#Dar de baja a un cliente
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.estatus = False  # Desactivar
    cliente.save()
    return redirect('pageclientes')


# Reactivar un cliente
def reactivar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.estatus = True  # Volver a activar
    cliente.save()
    return redirect('pageclientes')