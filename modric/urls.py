from django.urls import path
from .views import index

app_name = 'modric'

urlpatterns = [
    path('', index, name='index'),
    ]
