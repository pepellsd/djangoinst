from django.db import models
from django.conf import settings
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, null=True)
    tags = models.ManyToManyField('Tag', db_index=True)
    images = models.ManyToManyField('Picture')

    def __str__(self):
        return f"post of {self.user}, id: {self.pk}"

    def absolute_url(self):
        return reverse('view_post', kwargs={"pk": self.pk})

    def get_likes(self):
        return Like.objects.filter(post_id=self.pk).count()


class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "post"]
        index_together = ["user", "post"]


class Picture(models.Model):
    path = models.ImageField(upload_to="photos/")


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=500)
