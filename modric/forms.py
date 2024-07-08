from django import forms

from .models import Partido, Invitacion, Comunidad
from accounts.models import CustomUser


class PartidoForm(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha')
    hora = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Hora')

    class Meta:
        model = Partido

        fields = ['deporte', 'fecha', 'hora', 'duracion_personalizada', 'recinto', 'nombre_pista', 'cubierto',
                  'precio_pista', 'precio_jugador', 'administradores', 'integrantes',
                  'integrantes_local', 'integrantes_visitante', 'color_local', 'color_visitante', 'resultado_estado',
                  'marcador_local', 'marcador_visitante', 'visibilidad', 'comunidad']

    def __init__(self, *args, **kwargs):
        # Obtener la instancia del partido actual
        partido = kwargs.get('instance')
        # Obtener el usuario actual
        user = kwargs.pop('user', None)
        # Edicion
        marcador = kwargs.pop('marcador', False)
        super(PartidoForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
                field.label_suffix = ''
                self.fields[field_name].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
            else:
                if field.widget.attrs.get('class'):
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'

        if not marcador:
            self.fields['resultado_estado'].label = ''
            self.fields['resultado_estado'].widget = forms.HiddenInput()
            self.fields['marcador_local'].label = ''
            self.fields['marcador_local'].widget = forms.HiddenInput()
            self.fields['marcador_visitante'].label = ''
            self.fields['marcador_visitante'].widget = forms.HiddenInput()
            self.fields['resultado_estado'].initial = Partido.E
            self.fields['marcador_local'].initial = 0
            self.fields['marcador_visitante'].initial = 0

        if user:
            comunidades = Comunidad.objects.filter(miembros=user).order_by('nombre')
            self.fields['comunidad'].queryset = comunidades

            miembros = (CustomUser.objects.filter(miembros_comunidad__in=comunidades)
                                                   .distinct().order_by('username'))
            self.fields['administradores'].queryset = miembros
            self.fields['integrantes'].queryset = miembros
            self.fields['integrantes_local'].queryset = miembros
            self.fields['integrantes_visitante'].queryset = miembros

        if partido:
            # Filtrar los usuarios que forman parte de 'integrantes'
            self.fields['integrantes_local'].queryset = partido.integrantes.all().order_by('username')
            self.fields['integrantes_visitante'].queryset = partido.integrantes.all().order_by('username')


class InvitacionForm(forms.ModelForm):
    class Meta:
        model = Invitacion
        fields = ['comunidad', 'usuario']

    def __init__(self, user, *args, **kwargs):
        super(InvitacionForm, self).__init__(*args, **kwargs)
        self.fields['comunidad'].queryset = Comunidad.objects.filter(administradores=user).order_by('nombre')
        # Si sobrase tiempo, sería conveniente excluir los miembros de las comunidades seleccionadas en el primer campo
        self.fields['usuario'].queryset = CustomUser.objects.exclude(id=user.id).order_by('username')


class ComunidadForm(forms.ModelForm):
    class Meta:
        model = Comunidad
        fields = ['nombre', 'escudo', 'descripcion', 'administradores', 'miembros']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'escudo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'administradores': forms.SelectMultiple(attrs={'class': 'form-control w-100', 'style': 'height: 200px;'}),
            'miembros': forms.SelectMultiple(attrs={'class': 'form-control w-100', 'style': 'height: 200px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(ComunidadForm, self).__init__(*args, **kwargs)