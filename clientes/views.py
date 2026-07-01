from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Cliente

#create your views here.
def listaclientes(request):
    consultaclientes=Cliente.objects.all() 
    return render(request, 'clientes/clientes.html', {'consultaclientes': consultaclientes})

def createclientes(request):
    nvocliente=Cliente(
        nombre=request.POST['nombre'],
        apellido=request.POST['apellido'],
        sexo=request.POST['sexo'],
        tipo=request.POST['tipo'],
        direccion=request.POST['direccion']
    )
    nvocliente.save()
    return redirect('/pageclientes')


