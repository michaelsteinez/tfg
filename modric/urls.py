from django.urls import path
from modric.views import (index, crear_partido, buscar_partidos, listar_partidos, importar_usuarios_API,
                          detalle_partido, editar_partido, detalle_recinto, jugador_partido,
                          enviar_invitacion, manejar_solicitudes, solicitar_membresia, invitaciones_enviadas,
                          notificaciones, detalle_comunidad)

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

    path('enviar_invitacion/', enviar_invitacion, name='enviar_invitacion'),
    path('manejar_solicitudes/', manejar_solicitudes, name='manejar_solicitudes'),
    path('solicitar_membresia/<int:comunidad_id>/', solicitar_membresia, name='solicitar_membresia'),
    path('invitaciones_enviadas/', invitaciones_enviadas, name='invitaciones_enviadas'),
    path('notificaciones/', notificaciones, name='notificaciones'),
    path('detalle_comunidad/<int:comunidad_id>/', detalle_comunidad, name='detalle_comunidad'),

    path('starwars/', importar_usuarios_API, name='importar_starwars'),

    ]
