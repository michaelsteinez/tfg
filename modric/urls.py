from django.urls import path
from modric.views import (index, crear_partido, buscar_partidos, listar_partidos, importar_usuarios_API,
                          detalle_partido, editar_partido, detalle_recinto, jugador_partido)

app_name = 'modric'

urlpatterns = [
    path('', index, name='index'),

    path('partidos/', listar_partidos, name='ver_partidos'),
    path('partido/buscar/', buscar_partidos, name='buscar_partidos'),
    path('partido/crear/', crear_partido, name='crear_partido'),
    path('partido/ver_detalle/<int:pk>', detalle_partido, name='detalle_partido'),
    path('partido/editar/<int:pk>/', editar_partido, name='editar_partido'),

    path('partido/jugador_partido/', jugador_partido, name='jugador_partido'),

    path('recinto/<int:pk>/', detalle_recinto, name='recinto'),

    path('starwars/', importar_usuarios_API, name='importar_starwars'),

    ]
