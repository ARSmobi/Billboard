from allauth.account.forms import SignupForm
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import mail_admins, EmailMultiAlternatives


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name='Common_users')
        user.groups.add(common_users)

        subject = 'Добро пожаловать!'
        text = f'{user.username}, вы успешно зарегистрировались!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="{settings.SITE_URL}">новостном портале!</a>'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()

        mail_admins(
            subject='Новый пользователь',
            message=f'Пользователь {user.username} зарегистрировался на новостном портале.',
        )

        return user