import random
import string
from django.db import models
from django.utils import timezone
from datetime import timedelta


def _generate_otp():
    return "".join(random.choices(string.digits, k=6))


class EmailOTP(models.Model):
    """Stores a pending registration + 6-digit OTP until verified."""

    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, default=_generate_otp)
    # Hashed password (from Django password hasher) waiting for verification
    password_hash = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Email OTP"
        verbose_name_plural = "Email OTPs"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_locked(self):
        return self.attempts >= 5

    def __str__(self):
        return f"OTP for {self.email}"
