from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Deporte(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    num_jugadores = models.IntegerField(default=1)
    duracion_base = models.IntegerField(default=60) # Duración del encuentro en minutos típicos al alquilar una pista

    def __str__(self):
        return self.nombre


class Recinto(models.Model):
    nombre = models.CharField(max_length=60)
    municipio = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    pais = models.CharField(max_length=60)
    deportes = models.ManyToManyField(Deporte, related_name='recintos') # Lista de deportes practicables

    def __str__(self):
        return f"{self.nombre} ({self.municipio})"


class Partido(models.Model):
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    fecha = models.DateField()
    duracion_personalizada = models.IntegerField(default=60, verbose_name='Duración del encuentro') # Duración personalizada por el administrador
    recinto = models.ForeignKey(Recinto, on_delete=models.CASCADE)
    nombre_pista = models.CharField(max_length=60, blank=True, verbose_name='Número de pista')  # Pista dentro del recinto
    cubierto = models.BooleanField(default=False)  # A la intemperie o no
    precio_pista = models.FloatField(default=0, verbose_name='Precio total de la pista')
    precio_jugador = models.FloatField(default=0, verbose_name='Precio por jugador')

    administradores = models.ManyToManyField(CustomUser, related_name='administradores_partido', verbose_name='Organizadores')
    integrantes = models.ManyToManyField(CustomUser, related_name='integrantes_partido')
    integrantes_local = models.ManyToManyField(CustomUser, related_name='integrantes_local', verbose_name='Equipo local')
    integrantes_visitante = models.ManyToManyField(CustomUser, related_name='integrantes_visitante', verbose_name='Equipo visitante')
    color_local = models.CharField(max_length=60, blank=True, default='blanco')
    color_visitante = models.CharField(max_length=60, blank=True, default='azul')

    V = 'V'
    E = 'E'
    D = 'D'
    S = 'S'
    resultado_choices = (
        (V, 'Victoria local'),
        (E, 'Empate'),
        (D, 'Victoria visitante'),
        (S, 'Suspendido'),
    )
    resultado_estado = models.CharField(max_length=1, choices=resultado_choices, default='E', verbose_name='Resultado')
    marcador_local = models.IntegerField(default=0)
    marcador_visitante = models.IntegerField(default=0)

    def __str__(self):
        return f"Partido de {self.deporte} el {self.fecha}"

# Para ver los participantes
# partido = Partido.objects.get(id=1)
# integrantes = partido.integrantes.all()

# Para agregar un jugador a un partido
# usuario = CustomUser.objects.get(id=1)
# partido = Partido.objects.get(id=1)
# partido.integrantes.add(usuario)

# #####################################################################################
# class Comunidad(models.Model):
#     nombre = models.CharField(max_length=100, unique=True)
#     escudo = models.ImageField(upload_to='comunidads/')
#     descripcion = models.TextField()
#     administradores = models.ManyToManyField(CustomUser, related_name='administradores_comunidad')
#     miembros = models.ManyToManyField(CustomUser, related_name='miembros_comunidad')
