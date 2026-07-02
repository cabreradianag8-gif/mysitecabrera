from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto

#create your views here.
def listaproductos(request):
    consultaproductos=Producto.objects.all() 
    return render(request, 'productos/productos.html', {'consultaproductos': consultaproductos})

def createproductos(request):
    nvoproducto=Producto(
        nombre=request.POST['nombre'],
        precio=request.POST['precio'],
        stock=request.POST['stock'],
        descripcion=request.POST['descripcion'],
        categoria=request.POST['categoria']

    )
    nvoproducto.save()
    return redirect('/pageproductos')

