import random
import string
from django.db import models
from bboard.models import User


class VerificationCode(models.Model):
    code = models.CharField(max_length=10, unique=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_code')
    created_at = models.DateTimeField(auto_now_add=True)
    delete_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

    def generate_code(self):
        length = 10
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=length))

    def __str__(self):
        return self.code
