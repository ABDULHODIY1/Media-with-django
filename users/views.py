from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.shortcuts import render, redirect

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
