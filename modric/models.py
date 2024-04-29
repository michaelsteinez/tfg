from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Deporte(models.Model):
    nombre = models.CharField(max_length=60, null=False, blank=False, unique=True)


class Recinto(models.Model):
    nombre = models.CharField(max_length=60, null=False, blank=False)
    municipio = models.CharField(max_length=60, null=False, blank=False)
    provincia = models.CharField(max_length=60, null=False, blank=False)
    pais = models.CharField(max_length=60, null=False, blank=False)
