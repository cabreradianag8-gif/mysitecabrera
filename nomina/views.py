from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from decimal import Decimal
from .models import nomina
from empleados.models import empleados

def pagenomina_view(request, pk_editar=None):
    nomina_a_editar = None
    if pk_editar:
        nomina_a_editar = get_object_or_404(nomina, pk=pk_editar)

    lista_empleados = empleados.objects.filter(status=True).order_by('nombre')

    # --- NÓMINAS ACTIVAS ---
    query = request.GET.get('q', '')
    if query:
        consultanominas = nomina.objects.filter(
            numperiodo__icontains=query, status=True
        ).order_by('-id') | nomina.objects.filter(
            empleado__nombre__icontains=query, status=True
        ).order_by('-id')
    else:
        consultanominas = nomina.objects.filter(status=True).order_by('-id')
    
    paginator = Paginator(consultanominas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # --- NÓMINAS CANCELADAS ---
    query_inactivo = request.GET.get('q_inactivo', '')
    if query_inactivo:
        nominas_inactivas = nomina.objects.filter(
            numperiodo__icontains=query_inactivo, status=False
        ).order_by('-id') | nomina.objects.filter(
            empleado__nombre__icontains=query_inactivo, status=False
        ).order_by('-id')
    else:
        nominas_inactivas = nomina.objects.filter(status=False).order_by('-id')
        
    paginator_inactivo = Paginator(nominas_inactivas, 5)
    page_number_inactivo = request.GET.get('page_inactivo')
    page_obj_inactivo = paginator_inactivo.get_page(page_number_inactivo)
    
    context = {
        'consultanominas': page_obj,
        'query': query,
        'nominas_inactivas': page_obj_inactivo,
        'query_inactivo': query_inactivo,
        'nomina_a_editar': nomina_a_editar,
        'lista_empleados': lista_empleados
    }
    return render(request, 'nomina/nomina.html', context)


def nueva_nomina(request):
    if request.method == 'POST':
        empleado_id = request.POST.get('empleado_id')
        empleado_instancia = get_object_or_404(empleados, pk=empleado_id)
        
        # 1. Automatizar Fecha (Hoy)
        fecha_hoy = timezone.now().date()
        
        # 2. Automatizar Número de Periodo (Q1 o Q2 según el día del mes)
        meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
        quincena = "Q1" if fecha_hoy.day <= 15 else "Q2"
        periodo_auto = f"{quincena}-{meses[fecha_hoy.month - 1]}-{fecha_hoy.year}"
        
        # 3. Extraer montos financieros
        salario = Decimal(request.POST.get('salario', '0'))
        percepciones = Decimal(request.POST.get('percepciones', '0'))
        deducciones = Decimal(request.POST.get('deducciones', '0'))
        
        # 4. Automatizar Monto Total Neto
        total_calculado = salario + percepciones - deducciones
        
        nomina.objects.create(
            numperiodo=periodo_auto,
            fecha=fecha_hoy,
            salario=salario,
            percepciones=percepciones,
            deducciones=deducciones,
            total=total_calculado,
            empleado=empleado_instancia
        )
    return redirect('rutapagenomina')


def actualizar_nomina(request, pk):
    recibo = get_object_or_404(nomina, pk=pk)
    if request.method == 'POST':
        empleado_id = request.POST.get('empleado_id')
        recibo.empleado = get_object_or_404(empleados, pk=empleado_id)
        
        recibo.salario = Decimal(request.POST.get('salario', '0'))
        recibo.percepciones = Decimal(request.POST.get('percepciones', '0'))
        recibo.deducciones = Decimal(request.POST.get('deducciones', '0'))
        
        # Recalcular el total automáticamente en la edición por si cambiaron los valores
        recibo.total = recibo.salario + recibo.percepciones - recibo.deducciones
        recibo.save()
    return redirect('rutapagenomina')


def eliminar_nomina(request, pk):
    recibo = get_object_or_404(nomina, pk=pk)
    recibo.status = False
    recibo.save()
    return redirect('rutapagenomina')


def reactivar_nomina(request, pk):
    recibo = get_object_or_404(nomina, pk=pk)
    recibo.status = True
    recibo.save()
    return redirect('rutapagenomina')