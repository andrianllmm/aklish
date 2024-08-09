from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control mb-2", "autofocus": "true"}
            ),
            "email": forms.TextInput(
                attrs={"required": "true", "class": "form-control mb-2"}
            ),
            "first_name": forms.TextInput(
                attrs={"required": "true", "class": "form-control mb-2"}
            ),
            "last_name": forms.TextInput(
                attrs={"required": "true", "class": "form-control mb-2"}
            ),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control mb-2"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control mb-2"})
    )


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control mb-2", "autofocus": "true"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control mb-2"})
    )
