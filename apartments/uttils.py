from typing import Final

import requests
from django.conf import settings
from django.db import transaction
from requests import Response
from rest_framework.utils import json

from apartments.models import Apartment, City, ApartmentService, ApartmentPhoto


class RealCalendarConnectionException(Exception):
    """Не удалось установить соединение с модулем бронирования"""


class RealCalendarAPIException(Exception):
    """Получен некорректный ответ от модуля бронирования"""


class RealtyCalendar:
    ALL_APARTMENTS_URL: Final[
        str] = f'{settings.REALTY_CALENDAR_HOST}/widgets/bookings/search/{settings.REALTY_CALENDAR_CLIENT_JSON}'

    @classmethod
    def __save_apartment_photos(cls, apartment: Apartment, apartment_json: dict) -> None:
        for photo in apartment_json['photos']:
            ApartmentPhoto.objects.create(
                apartment=apartment,
                photo_url=photo['file']
            )

    @classmethod
    def __synchronize_apartments_by_real_calendar_json(cls, response_json: json) -> list:
        new_added_apartments = []
        for apartment in response_json['apartments']:
            if not Apartment.objects.filter(real_calendar_id=apartment['id']).exists():
                new_added_apartments.append(apartment["id"])

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

                    cls.__save_apartment_photos(
                        apartment=apartment_record,
                        apartment_json=apartment
                    )

        return new_added_apartments

    @classmethod
    def download_apartments_info(cls) -> list[str]:
        request_url = cls.ALL_APARTMENTS_URL

        try:
            response = requests.get(request_url)

            if response.status_code == 200:
                response_json = response.json()
                new_added_apartments = cls.__synchronize_apartments_by_real_calendar_json(response_json)
                return new_added_apartments
            else:
                raise RealCalendarAPIException()
        except (requests.exceptions.ConnectionError, RealCalendarAPIException) as exception_type:
            match exception_type.__class__.__name__:
                case RealCalendarConnectionException.__name__:
                    print("Не удалось установить соединение с модулем бронирования")
                case requests.exceptions.ConnectionError.__class__.__name__:
                    print("Не удалось установить соединение")
                case RealCalendarAPIException.__name__:
                    print("Некорректный ответ от API")

    @classmethod
    def get_apartments_in_date_range(cls, begin_date, end_date, city_ids=None, humans=1):
        request_url = f'{cls.ALL_APARTMENTS_URL}?begin_date={begin_date}&end_date={end_date}&humans={humans}&city_ids[]={city_ids}'

        if city_ids is None:
            request_url = f'{cls.ALL_APARTMENTS_URL}?begin_date={begin_date}&end_date={end_date}&humans={humans}'

        response_json = requests.get(request_url).json()
        cls.__synchronize_apartments_by_real_calendar_json(response_json)

        apartments_ids = []
        for apartment in response_json['apartments']:
            apartments_ids.append(apartment['id'])

        return apartments_ids

    @classmethod
    def get_price_for_apartment(cls, begin_date: str, end_date: str, apartment_id: int, humans: int = 0) -> dict:
        GET_APARTMENTS_PRICE_URL: Final[str] = (
            f'{settings.REALTY_CALENDAR_HOST}/'
            f'widgets/bookings/apartments/{apartment_id}/'
            f'price.json?token={settings.REALTY_CALENDAR_CLIENT_JSON}'
        )

        REQUEST_URL: Final[str] = (
            f'{GET_APARTMENTS_PRICE_URL}'
            f'&humans={humans}'
            f'&begin_date={begin_date}'
            f'&end_date={end_date}'
            f'&apartment_id={apartment_id}'
        )
        response: Response = requests.get(REQUEST_URL)
        if response.status_code == 200:
            response_json = response.json()
            return response_json
        else:
            return {
                'status_code': response.status_code,
            }


