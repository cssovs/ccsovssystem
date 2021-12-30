from django import forms
from django.contrib.auth import models
from django.contrib.auth.models import User

from settings.models import Student


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    # profile = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password']
        widgets = {
            'password': forms.PasswordInput,
        }
