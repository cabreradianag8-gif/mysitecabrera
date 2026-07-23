from django.contrib import admin
from .models import grupos_usuarios

class GruposUsuariosAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'nombre', 'correo', 'grupo', 'empleado', 'estatus')
    search_fields = ('usuario', 'nombre', 'correo', 'grupo__nombre')  
    list_filter = ('estatus', 'grupo')                                
    ordering = ('id',)

admin.site.register(grupos_usuarios, GruposUsuariosAdmin)