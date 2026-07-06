from django.shortcuts import render

def home(request):
    # Esta vista solo carga una plantilla HTML llamada 'home.html'
    return render(request, 'home/home.html')
