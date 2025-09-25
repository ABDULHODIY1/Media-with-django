from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .forms import EditProfileForm

User = get_user_model()


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "registration/register.html", {
                "error": "Bunday foydalanuvchi allaqachon mavjud."
            })
        elif not username or not password:
            return render(request, "registration/register.html", {
                "error": "Iltimos, barcha maydonlarni to‘ldiring."
            })

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('app:home')

    return render(request, "registration/register.html")


class EditProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = "changeProfile/chp.html"
    success_url = reverse_lazy("app:home")

    def get_object(self, queryset=None):
        return self.request.user
