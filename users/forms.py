from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()  # ✅ Bu joy muhim!
        fields = ('username', 'email', 'password1', 'password2')
from django import forms
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # qaysi fieldlarni edit qilishni xohlasangiz yozasiz
