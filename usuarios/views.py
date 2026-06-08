from django.shortcuts import render
from django.http import HttpResponse

#create your views here.
def usuarios(request):
    #return HttpResponse("FORMULARIO DE USUARIOS-DIANA")
    return render(request, 'usuarios/usuarios.html')
