from django.db import models
from accounts.models import CustomUser


class Comunidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    escudo = models.ImageField(upload_to='comunidades/', blank=True)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    administradores = models.ManyToManyField(CustomUser, related_name='administradores_comunidad')
    miembros = models.ManyToManyField(CustomUser, related_name='miembros_comunidad')

    class Meta:
        verbose_name = 'Comunidad'
        verbose_name_plural ='Comunidades'

    def __str__(self):
        return self.nombre


# Create your models here.
class Deporte(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    num_jugadores = models.IntegerField(default=1)
    duracion_base = models.IntegerField(default=60) # Duración del encuentro en minutos típicos al alquilar una pista

    def __str__(self):
        return self.nombre


class Recinto(models.Model):
    nombre = models.CharField(max_length=60)
    calle = models.CharField(max_length=120, blank=True)
    municipio = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    pais = models.CharField(max_length=60)
    deportes = models.ManyToManyField(Deporte, related_name='recintos') # Lista de deportes practicables

    def __str__(self):
        return f"{self.nombre} ({self.municipio})"


# A la clase Partido le falta un atributo "creador" que no puede estar vacío y un atributo dirección
class Partido(models.Model):
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    duracion_personalizada = models.IntegerField(default=60, verbose_name='Duración del encuentro') # Duración personalizada por el administrador
    recinto = models.ForeignKey(Recinto, on_delete=models.CASCADE)
    nombre_pista = models.CharField(max_length=60, blank=True, verbose_name='Número de pista')  # Pista dentro del recinto
    cubierto = models.BooleanField(default=False)  # A la intemperie o no
    precio_pista = models.FloatField(default=0, verbose_name='Precio total de la pista')
    precio_jugador = models.FloatField(default=0, verbose_name='Precio por jugador')

    creador = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    administradores = models.ManyToManyField(CustomUser, related_name='administradores_partido', verbose_name='Organizadores')
    integrantes = models.ManyToManyField(CustomUser, related_name='integrantes_partido', blank=True, verbose_name='Integrantes')
    # Falta controlar que un jugador no pueda estar en el equipo local y en el visitante a la vez
    # Ambos deben pertener a integrantes (quizas usando sets?)
    # Habrá que borrar antes los partidos existentes para tener la base de datos limpia
    integrantes_local = models.ManyToManyField(CustomUser, related_name='integrantes_local', blank=True, verbose_name='Equipo local')
    integrantes_visitante = models.ManyToManyField(CustomUser, related_name='integrantes_visitante', blank=True, verbose_name='Equipo visitante')
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
    # Si sobrase tiempo, este marcador habrá que adaptarlo a pádel y tenis para recoger como fueron los juegos
    # y los posibles tie-break
    marcador_local = models.IntegerField(default=0)
    marcador_visitante = models.IntegerField(default=0)

    A = 'A'
    P = 'P'
    visibilidad_choices = (
        (A, 'Público'),
        (P, 'Privado'),
    )
    visibilidad = models.CharField(max_length=1, choices=visibilidad_choices, default='A', verbose_name='Visibilidad')
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, null=True)

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
