from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.conf import settings


class User(AbstractUser):
    username = None
    email = models.EmailField(db_index=True, unique=True)
    bio = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to="photos/", null=True)
    images = models.ManyToManyField('instagram.Picture')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email


class Token(models.Model):
    code = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField()