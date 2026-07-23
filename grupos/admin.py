from django.contrib import admin
from .models import grupos_grupos

class GruposGruposAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'fecha_creacion', 'estatus')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('estatus', 'fecha_creacion')
    ordering = ('id',)

admin.site.register(grupos_grupos, GruposGruposAdmin)