from django.utils.translation import gettext as _

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import News, User

@receiver(post_save, sender=News)
def send_news_email(sender, instance, created, **kwargs):
    if created:
        subject = _(f'Последняя новость: {instance.title}')
        message = _(f'Текст новости: {instance.text}')
        from_email = 'note@site.ru'
        to_emails = User.objects.values_list('email', flat=True)
        send_mail(subject, message, from_email, to_emails)
