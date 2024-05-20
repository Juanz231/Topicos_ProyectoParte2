from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Ropa, Regalo

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['tipo_usuario'].widget = forms.Select(choices=CustomUser.TIPO_USUARIO_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'tipo_usuario')


class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)


class RegaloForm(forms.ModelForm):
    class Meta:
        model = Regalo
        fields = '__all__'



class RopaForm(forms.ModelForm):
    class Meta:
        model = Ropa
        fields = '__all__'  # Esto incluirá todos los campos del modelo Ropa en el formulario

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 0:
            raise ValidationError("El precio no puede ser negativo")
        return precio