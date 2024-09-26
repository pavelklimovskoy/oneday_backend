from django.contrib.auth.models import AbstractUser
from django.db import models
from pip._internal.utils._jaraco_text import _

from apartments.models import Apartment


class UserProfile(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default=None)
    birth_date = models.DateTimeField(_("birth date"), blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    telegram_nickname = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)

    bonus_points = models.IntegerField(blank=True, null=True, default=0)

    favorites_apartments = models.ManyToManyField(Apartment, blank=True, related_name='favorites_apartments', null=True,
                                                  default=None)

    def __str__(self):
        return f'{self.id} {self.username} {self.phone_number}'


class BookingRecord(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='booking_history')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='booked_users')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.user_profile} {self.apartment} {self.start_date} {self.end_date}'
