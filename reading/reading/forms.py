import django
from django import forms
from .models import CustomUser








from django import forms
from django.contrib.auth import authenticate


from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from social_core.backends.facebook import FacebookOAuth2
from social_core.backends.twitter import TwitterOAuth
from social_core.backends.google import GoogleOAuth2


#from social_core.backends.utils import load_backend


from django.contrib.auth.backends import ModelBackend
from social_core.backends.facebook import FacebookOAuth2
from social_core.backends.twitter import TwitterOAuth
from social_core.backends.google import GoogleOAuth2

from django.contrib.auth.backends import ModelBackend

authentication_backends = [
    ModelBackend,  # Default Django authentication backend
    FacebookOAuth2,
    TwitterOAuth,
    GoogleOAuth2,
    ]

from django import forms
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password_confirmation': forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}),
        }
class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password', 'password_confirmation')

    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")

        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken")

        user = None
        for backend in authentication_backends:
            user = backend().authenticate(
                request=None,  # Pass a dummy request object
                email=email,
                password=password,
            )
            if user is not None:
                break

        if user is None:
            raise forms.ValidationError("Invalid email or password")

        return cleaned_data



# Créer un formulaire d'authentification pour collecter les informations d'authentification de l'utilisateur
from django.contrib.auth.forms import AuthenticationForm

class SignInForm(AuthenticationForm):
    name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    email = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


from django.db import models



