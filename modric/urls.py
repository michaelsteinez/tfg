from django.urls import path
from modric.views import index, crear_partido, listar_partidos, importar_usuarios_API

app_name = 'modric'

urlpatterns = [
    path('', index, name='index'),
    path('crear_partido/', crear_partido, name='crear_partido'),
    path('ver_partidos/', listar_partidos, name='ver_partidos'),
    path('starwars/', importar_usuarios_API, name='importar_starwars'),
    ]
