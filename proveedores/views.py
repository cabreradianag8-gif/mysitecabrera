from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Proveedores

#create your views here.
def listaproveedores(request):
    consultaproveedores=Proveedores.objects.all() 
    return render(request, 'proveedores/proveedores.html', {'consultaproveedores': consultaproveedores})

def createproveedores(request):
    nvoproveedor=Proveedores(
        nombre=request.POST['nombre'],
        direccion=request.POST['direccion'],
        telefono=request.POST['telefono'],
        email=request.POST['email'],
        categoria=request.POST['categoria']
    )
    nvoproveedor.save()
    return redirect('/pageproveedores')
