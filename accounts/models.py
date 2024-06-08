from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    altura = models.PositiveSmallIntegerField(null=True, blank=True)
    fecha_nac = models.DateField(null=True, blank=True, verbose_name="Fecha de nacimiento")
    V = 'V'
    M = 'M'
    sexo_choices = (
        (V, 'Varón'),
        (M, 'Mujer'),
    )
    sexo = models.CharField(max_length=1, choices=sexo_choices, default='V')

    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    username = models.CharField(max_length=150, unique=True, verbose_name='Nombre de usuario')

    def __str__(self):
        return self.username

