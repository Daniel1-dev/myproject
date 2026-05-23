from django.db import models
from django.contrib.auth.models import User 
# Create your models here.


# User profile
class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_picture = models.ImageField(
        upload_to='profiles/',
        default='profiles/default.png'
    )

    bio = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.user.username


# Notes model
class Note(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=100
    )

    content = models.TextField()

    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title