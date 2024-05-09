from django.urls import path
from .views import index, crear_partido

app_name = 'modric'

urlpatterns = [
    path('', index, name='index'),
    path('crear_partido/', crear_partido, name='crear_partido'),
    ]
