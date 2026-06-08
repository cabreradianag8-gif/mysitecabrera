from django.shortcuts import render
from django.http import HttpResponse

#create your views here.
def productos(request):
    #return HttpResponse("FORMULARIO DE PRODUCTOS-DIANA")
    return render(request, 'productos/productos.html')

