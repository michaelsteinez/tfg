from django.db import models


# Create your models here.
class Usuario(models.Model):
    username = models.CharField(max_length=12, null=False, blank=False, unique=True)
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=100)
    fecha_nac = models.DateField()
    V = 'V'
    M = 'M'
    sexo_choices = (
        (V, 'Varón'),
        (M, 'Mujer'),
    )
    sexo = models.CharField(max_length=1, choices=sexo_choices, default='V')


class Deporte(models.Model):
    nombre = models.CharField(max_length=60, null=False, blank=False, unique=True)


class Recinto(models.Model):
    nombre = models.CharField(max_length=60, null=False, blank=False)
    municipio = models.CharField(max_length=60, null=False, blank=False)
    provincia = models.CharField(max_length=60, null=False, blank=False)
    pais = models.CharField(max_length=60, null=False, blank=False)
