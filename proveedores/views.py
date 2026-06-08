from django.shortcuts import render
from django.http import HttpResponse

#create your views here.
def proveedores(request):
    #return HttpResponse("FORMULARIO DE PROVEEDORES-DIANA")
    return render(request, 'proveedores/proveedores.html')
