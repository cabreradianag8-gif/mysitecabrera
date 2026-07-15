from usuarios.models import grupos_usuarios  

def roles_usuario(request):
    """
    Este procesador inyecta los roles del usuario de manera global
    en todas las plantillas del proyecto.
    """
    if not request.user.is_authenticated:
        return {}

    usuario_actual = request.user
    
    # Buscamos su rol en tu tabla de perfiles
    mi_usuario_perfil = grupos_usuarios.objects.filter(usuario=usuario_actual.username, estatus=True).first()
    
    es_admin = False
    es_almacenista = False
    es_cajera = False
    
    if mi_usuario_perfil and mi_usuario_perfil.grupo:
        nombre_grupo = mi_usuario_perfil.grupo.nombre.lower()
        if 'admin' in nombre_grupo:
            es_admin = True
        elif 'almacen' in nombre_grupo or 'prov' in nombre_grupo or 'compras' in nombre_grupo:
            es_almacenista = True
        elif 'caja' in nombre_grupo or 'venta' in nombre_grupo:
            es_cajera = True

    if usuario_actual.is_superuser:
        es_admin = True

    return {
        'es_admin': es_admin,
        'es_almacenista': es_almacenista,
        'es_cajera': es_cajera,
        'perfil': mi_usuario_perfil
    }