from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254, blank=False, null=False)

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(_("Birth Date (optional)"), blank=True, null=True)
    bio = models.CharField(_("Bio"), max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(
        _("Set your profile picture"),
        upload_to="profpictures/%Y/%m/%d/",
        blank=True,
        null=True
    )
    def __str__(self):
        return self.username
