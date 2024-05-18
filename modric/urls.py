from django.urls import path
from modric.views import index, crear_partido, listar_partidos, importar_usuarios_API, detalle_partido

app_name = 'modric'

urlpatterns = [
    path('', index, name='index'),

    path('partidos/', listar_partidos, name='ver_partidos'),
    path('partido/crear/', crear_partido, name='crear_partido'),
    path('partido/ver_detalle/<int:id>', detalle_partido, name='detalle_partido'),

    path('starwars/', importar_usuarios_API, name='importar_starwars'),

    ]
