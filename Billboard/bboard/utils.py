from django.utils import timezone
from datetime import timedelta
from .models import User, Subscription


def is_user_online(user):
    if user.last_activity:
        return timezone.now() - user.last_activity < timedelta(minutes=5)
    return False


def get_online_users():
    return User.objects.filter(last_activity__gt=timezone.now() - timedelta(minutes=5))
