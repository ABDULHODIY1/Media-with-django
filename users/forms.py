from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()  # ✅ Bu joy muhim!
        fields = ('username', 'email', 'password1', 'password2')
