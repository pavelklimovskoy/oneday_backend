from typing import Final

from django.conf import settings
from django.contrib.sites import requests
import requests
from django.db import transaction
from rest_framework.utils import json

from apartments.models import Apartment, City, ApartmentService, ApartmentPhoto


class RealtyCalendar:
    ALL_APARTMENTS_URL: Final[
        str] = f'{settings.REALTY_CALENDAR_HOST}/widgets/bookings/search/{settings.REALTY_CALENDAR_CLIENT_JSON}'

    @classmethod
    def download_apartments_info(cls):
        request_url = cls.ALL_APARTMENTS_URL
        response_json = requests.get(request_url).json()

        for apartment in response_json['apartments']:
            if not Apartment.objects.filter(id=apartment['id']).exists():
                print(f'{apartment["id"]} does not exist')

                city_id = apartment['city']['id']

                with transaction.atomic():
                    if not City.objects.filter(real_calendar_id=city_id).exists():
                        City.objects.create(real_calendar_id=city_id, title=apartment['city']['title'])
                    else:
                        City.objects.filter(real_calendar_id=city_id).first()

                    apartment_record = Apartment.objects.create(
                        real_calendar_id=apartment['id'],
                        address=apartment['address'],
                        rooms=apartment['rooms'],
                        sleeps=apartment['sleeps'],
                        desc=apartment['desc'],
                        floor=apartment['floor'],
                        humans=apartment['humans'],
                        title=apartment['title'],
                        price=apartment['price'],
                        city=City.objects.get(real_calendar_id=city_id),
                        main_photo=apartment['main_photo']['preview']['url']
                    )

                    for service in apartment['services']:
                        if not ApartmentService.objects.filter(service_name=service['name']).exists():
                            service_record = ApartmentService.objects.create(
                                service_name=service['name'],
                                service_title=service['title'],
                            )
                            apartment_record.services.add(service_record)
                        else:
                            service_record = ApartmentService.objects.get(service_name=service['name'])
                            apartment_record.services.add(service_record)

                    for photo in apartment['photos']:
                        ApartmentPhoto.objects.create(
                            apartment=apartment_record,
                            photo_url=photo['file']
                        )


