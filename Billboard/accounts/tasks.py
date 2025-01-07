from celery import shared_task
from django.utils import timezone

from .models import VerificationCode
from ..bboard.models import User


@shared_task(name="accounts.tasks.delete_expired_verification_codes")
def delete_expired_verification_codes():
    VerificationCode.objects.filter(delete_at__lt=timezone.now()).delete()

@shared_task(name="accounts.tasks.send_verification_code")
def delete_unconfirmed_accounts():
    User.objects.filter(is_active=False, last_login=None).delete()
