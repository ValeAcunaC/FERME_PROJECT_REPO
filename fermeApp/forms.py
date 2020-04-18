from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    username = forms.EmailField(max_length=100)
    class Meta:
        model = User
        fields = ['username','password1','password2']