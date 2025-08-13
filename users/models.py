from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _



class CustomUser(AbstractUser):
    
    username = models.CharField(
        # _("Username (required)"), 
        max_length = 100, 
        unique = True,
        blank = False,
        null = False,
    )
    email = models.EmailField(
        # _("Email Address (required)"), 
        max_length = 254, 
        blank = False,
        null = False,
    )
    phone_number = models.CharField(
        # _("Phone Number (optional)"),
     max_length=20, 
     blank=True, 
     null=True)
    birth_date = models.DateField(
        _("Birth Date (optional)"),
         blank=True, null=True)
    
    # new fields
    bio = models.CharField(_("Bio"),
    max_length = 100, 
    blank = True,
    null = True,
    )
    
    profile_picture = models.ImageField(
        _("Set your profile picture"), 
        upload_to="media/profpictures",
        blank = True,
        null = True)

    def __str__(self):
        return self.username
