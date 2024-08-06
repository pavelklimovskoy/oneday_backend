from django.db import models
from django.db.models.fields import TextField
from django.forms import CharField, IntegerField, DateField, DateTimeField


class BookingAnalytics(models.Model):
    __slots__: tuple[str, ...] = (
        'phone',
        'amount',
        'fullname',
        'email',
        'begin_date',
        'end_date',
        'apartment_id',
        'created_at',
        'json_data',
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    phone: CharField = models.CharField(max_length=50, null=True, blank=True)
    amount: IntegerField = models.IntegerField(null=True, blank=True)
    fullname: CharField = models.CharField(max_length=50, null=True, blank=True)
    email: CharField = models.CharField(max_length=50, null=True, blank=True)
    begin_date: DateField = models.DateField(null=True, blank=True)
    end_date: DateField = models.DateField(null=True, blank=True)
    apartment_id: IntegerField = models.IntegerField(null=True, blank=True, default=None)
    created_at: DateTimeField = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    json_data: TextField = models.TextField(null=True, blank=True, default=None)
