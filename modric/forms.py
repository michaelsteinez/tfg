# En tu archivo forms.py
from django import forms
from .models import CustomUser

class RegistroForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # POR HACER: Controlar como entra la fecha y los numeros en apellidos y nombre
        fields = ['username', 'first_name', 'last_name', 'email', 'fecha_nacimiento', 'sexo']
