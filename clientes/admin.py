from django.contrib import admin
from .models import Cliente

# Register your models here.
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'sexo', 'tipo', 'direccion')
    search_fields = ('nombre', 'apellido', 'direccion')  
    list_filter = ('sexo', 'tipo')                      
    ordering = ('id',)                                   

admin.site.register(Cliente, ClienteAdmin)