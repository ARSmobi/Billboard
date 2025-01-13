from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext as _


class User(AbstractUser):
    is_active = models.BooleanField(default=False)
    GENDER = (
        ('m', _('Мужской')),
        ('f', _('Женский')),
    )
    gender = models.CharField(max_length=1, choices=GENDER, default='')
    birthday = models.DateTimeField(null=True)
    avatar = models.CharField(max_length=20, default='default.svg')
    last_activity = models.DateTimeField(default=timezone.now)

    def update_last_activity(self):
        self.last_activity = timezone.now()
        self.save()

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    def is_user_online(self, request):
        last_activity = request.session.get('last_activity')
        if last_activity:
            last_activity_time = timezone.datetime.fromisoformat(last_activity)
            return timezone.now() - last_activity_time < timedelta(minutes=5)
        return False


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
        subject = _('Отклик принят')
        message = _(f'Ваш отклик на объявление {adv.title} был принят.')
        from_email = 'note@site.ru'
        to_email = User.objects.get(id=self.user.id).email
        if self.accepted:
            self.accepted = False
        else:
            self.accepted = True
            send_mail(subject, message, from_email, [to_email])
        self.save()


class News(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField()
    text_html = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    tag = models.CharField(max_length=100)
