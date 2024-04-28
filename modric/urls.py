from django.urls import path
from .views import index, registro, registro_exito

app_name = 'modric'

urlpatterns = [
    path('', index, name='index'),
    path('registro/', registro, name='registro'),
    path('registro-exito/', registro_exito, name='registro_exito'),
    ]
