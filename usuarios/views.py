from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import usuario

#create your views here.
def listausuarios(request):
    consultausuarios=usuario.objects.all() 
    return render(request, 'usuarios/usuarios.html', {'consultausuarios': consultausuarios})

def createusuarios(request):
    nvousuario=usuario(
        nombre=request.POST['nombre'],
        apellido=request.POST['apellido'],
        cargo=request.POST['cargo'],
        email=request.POST['email'],
        password=request.POST['password']
        
    )
    nvousuario.save()
    return redirect('/pageusuarios')