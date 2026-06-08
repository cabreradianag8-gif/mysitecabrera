from django.shortcuts import render
from django.http import HttpResponse

#create your views here.
def clientes(request):
    #return HttpResponse("FORMULARIO DE CLIENTES-DIANA")
    return render(request, 'clientes/clientes.html')
