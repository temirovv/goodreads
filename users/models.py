from django.db.models import ImageField
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    profile_picture = ImageField(default='default_profile_pic.jpg')


