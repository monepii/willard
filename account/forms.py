from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario, Direccion

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd.get('password2')

class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['nombre', 'apellido', 'telefono', 'email']

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = [
            'calle', 'numero_exterior', 'numero_interior',
            'colonia', 'municipio', 'estado', 'codigo_postal', 'pais',
            'telefono', 'instrucciones', 'es_principal'
        ]
        widgets = {
            'calle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la calle'
            }),
            'numero_exterior': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número exterior'
            }),
            'numero_interior': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número interior (opcional)'
            }),
            'colonia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Colonia'
            }),
            'municipio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Municipio o Delegación'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estado'
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código Postal'
            }),
            'pais': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'País'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono de contacto (opcional)'
            }),
            'instrucciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Instrucciones especiales de entrega (opcional)'
            }),
            'es_principal': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que el campo país tenga un valor por defecto
        if not self.instance.pk:  # Solo para nuevas direcciones
            self.fields['pais'].initial = 'México'