from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import empleados

#create your views here.
def listaempleados(request):
    consultaempleados=empleados.objects.all() 
    return render(request, 'empleados/empleados.html', {'consultaempleados': consultaempleados})

def createempleados(request):
    nvoempleado=empleados(
        nombre=request.POST['nombre'],
        apellido=request.POST['apellido'],
        telefono=request.POST['telefono'],
        email=request.POST['email'],
        turno=request.POST['turno'],
        status=request.POST['status']
        
    )
    nvoempleado.save()
    return redirect('/pageempleados')