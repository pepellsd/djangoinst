from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from .manager import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(db_index=True, unique=True)
    bio = models.CharField(max_length=150, null=True)
    avatar = models.ImageField(upload_to="photos/", null=True)
    images = models.ManyToManyField('Picture')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email


class Token(models.Model):
    code = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField()


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null=True)
    tags = models.ManyToManyField('Tag', db_index=True)
    images = models.ManyToManyField('Picture')

    def absolute_url(self):
        return reverse('view_post', kwargs={"post_id": self.pk})

    def get_likes(self):
        return Like.objects.filter(post_id=self.pk).count()

    def get_comments(self):
        return Comment.objects.filter(post_id=self.pk)


class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    class Meta:
        unique_together=["user", "post"]
        index_together=["user", "post"]


class Picture(models.Model):
    path = models.ImageField(upload_to="photos/")


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
