from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta
from rest_framework.exceptions import ValidationError
import string
import secrets
from referral_code.settings import URL_REF_CODE

MAX_LENGTH_CODE = 10


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ref_code = models.URLField(null=True, blank=True)
    end_date_code = models.DateField(blank=True, null=True)
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='referrer')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        end_date = self.end_date_code
        if end_date and end_date < date.today() + timedelta(days=1):
            raise ValidationError("The date cannot be in the past!")
        super().save(*args, **kwargs)

    @staticmethod
    def get_ref_code():
        all_chars = string.ascii_letters + string.digits
        return URL_REF_CODE + ''.join(secrets.choice(all_chars) for i in range(MAX_LENGTH_CODE))
