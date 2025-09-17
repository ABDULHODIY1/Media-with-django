from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import EditProfileForm

from users.models import CustomUser

User = get_user_model()

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "registration/register.html", {
                "error": "Bunday foydalanuvchi allaqachon mavjud."
            })
        elif  not username or not password:
            return render(request, "registration/register.html", {
                "error": "Iltimos, barcha maydonlarni to‘ldiring."
                })

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('app:home')  # yoki kerakli sahifaga

    return render(request, "registration/register.html")


class EditProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = "changeProfile/chp.html"
    success_url = reverse_lazy("app:home")  # edit tugagach qaysi sahifaga o'tishi kerak
    context_object_name = "user"

    def get_object(self):
        # faqat hozirgi login bo'lgan userni qaytaramiz
        return self.request.user
