from celery import shared_task
from django.utils import timezone

from .models import VerificationCode

@shared_task(name="accounts.tasks.delete_expired_verification_codes")
def delete_expired_verification_codes():
    VerificationCode.objects.filter(delete_at__lt=timezone.now()).delete()
