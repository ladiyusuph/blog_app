from django import forms

# from django.contrib.auth.models import User
from .models import User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "avatar",
            "username",
            "email",
            "password1",
            "password2",
        ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "username", "email", "bio"]
        # widgets = {
        #     "password": forms.PasswordInput(),
        # }
