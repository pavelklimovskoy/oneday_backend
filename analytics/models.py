from django.db import models


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    phone = models.CharField(max_length=50, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    fullname = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    begin_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    apartment_id = models.IntegerField(null=True, blank=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    json_data = models.TextField(null=True, blank=True, default=None)
