from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail


class User(AbstractUser):
    GENDER = (
        ('m', 'Мужчина'),
        ('f', 'Женщина'),
    )
    gender = models.CharField(max_length=1, choices=GENDER, default='')
    birthday = models.DateTimeField(null=True)
    avatar = models.CharField(max_length=20, default='default.svg')

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

    def accept(self):
        adv = Advertisement.objects.get(id=self.advertisement.id)
        subject = f'Отклик принят'
        message = f'Ваш отклик на объявление {adv.title} был принят.'
        from_email = 'note@site.ru'
        to_email = User.objects.get(id=self.user.id).email
        if self.accepted:
            self.accepted = False
        else:
            self.accepted = True
            send_mail(subject, message, from_email, [to_email])
        self.save()
