from django.urls import path
from . import views

app_name = 'modric'

urlpatterns = [
    path('', views.index, name='index'),
    ]
