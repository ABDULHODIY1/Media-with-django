from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser


class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()  
        fields = ('username', 'email', 'password1', 'password2')
from django import forms
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username",'first_name', 'last_name', 'email',"bio","profile_picture"]

