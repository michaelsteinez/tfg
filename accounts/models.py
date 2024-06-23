from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


def resize_image(image_path, max_width=800, max_height=600):
    img = Image.open(image_path)
    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    img.save(image_path)


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
    foto = models.ImageField(upload_to='fotos/', null=True, blank=True, verbose_name="Foto de perfil")

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.foto:
            resize_image(self.foto.path)