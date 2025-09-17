from tkinter.font import names

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
import re
from .views import EditProfile

app_name = "users"
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html',), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path("edit/profile/<int:pk>/", EditProfile.as_view(), name="edprof"),
]
