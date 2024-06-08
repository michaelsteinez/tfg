from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    # class Meta:
    #     model = CustomUser
    #     fields = ("username", "email")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'altura', 'fecha_nac', 'sexo')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está registrado.")
        return username


class CustomUserChangeForm(UserChangeForm):
    fecha_nac = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha de nacimiento',
        required=False,
    )
    altura = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': '0'}),
        label='Altura en centímetros',
        required=False,
    )
    sexo = forms.ChoiceField(
        choices=CustomUser.sexo_choices,
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'altura', 'fecha_nac', 'sexo')

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control  form-control-lg"'
            else:
                field.widget.attrs['class'] = 'form-control'

        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['username'].widget.attrs['readonly'] = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está registrado.")
        return username
