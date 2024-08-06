from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER = (
        ('m', 'Мужчина'),
        ('f', 'Женщина'),
    )
    gender = models.CharField(max_length=1, choices=GENDER, default='')
    dateRegistration = models.DateTimeField(auto_now_add=True)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = models.TextField()
    content = RichTextUploadingField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    text = models.TextField()
    accepted = models.BooleanField(default=False)
    dateCreation = models.DateTimeField(auto_now_add=True)
