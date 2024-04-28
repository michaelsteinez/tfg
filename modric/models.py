from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    # Campos personalizados
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=10, choices=(('M', 'Masculino'), ('F', 'Femenino')), null=True, blank=True)

    # Especificar related_name para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user'
    )

    def __str__(self):
        return self.username


# class Usuario(models.Model):
#     username = models.CharField(max_length=12, null=False, blank=False, unique=True)
#     nombre = models.CharField(max_length=40)
#     apellidos = models.CharField(max_length=100)
#     fecha_nac = models.DateField()
#     V = 'V'
#     M = 'M'
#     sexo_choices = (
#         (V, 'Varón'),
#         (M, 'Mujer'),
#     )
#     sexo = models.CharField(max_length=1, choices=sexo_choices, default='V')


class Deporte(models.Model):
    nombre = models.CharField(max_length=60, null=False, blank=False, unique=True)


class Recinto(models.Model):
    nombre = models.CharField(max_length=60, null=False, blank=False)
    municipio = models.CharField(max_length=60, null=False, blank=False)
    provincia = models.CharField(max_length=60, null=False, blank=False)
    pais = models.CharField(max_length=60, null=False, blank=False)
