from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ("Qo‘shimcha ma'lumotlar", {
            "fields": (
                "phone_number",
                "birth_date",
                "bio",
                "profile_picture",
            ),
        }),
    )

    # Agar admin panelda "add user" formasini ham moslashtirmoqchi bo‘lsang:
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Qo‘shimcha ma'lumotlar", {
            "fields": (
                "phone_number",
                "birth_date",
                "bio",
                "profile_picture",
            ),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
