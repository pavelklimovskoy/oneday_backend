from typing import Final, Optional

import requests
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework.request import Request
from rest_framework.utils import json

from apartments.models import Apartment, City, ApartmentService, ApartmentPhoto


class RealCalendarPriceException(Exception):
    """Некорректный ответ от запроса ан получение цен"""


class RealCalendarConnectionException(Exception):
    """Не удалось установить соединение с модулем бронирования"""


class RealCalendarAPIException(Exception):
    """Получен некорректный ответ от модуля бронирования"""


class RealtyCalendar:
    ALL_APARTMENTS_URL: Final[
        str] = f'{settings.REALTY_CALENDAR_HOST}/widgets/bookings/search/{settings.REALTY_CALENDAR_CLIENT_JSON}'

    @classmethod
    def get_booking_form_data(cls, request: Request) -> dict:
        return json.loads(request.body.decode('utf-8'))

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
        request_url: Final[
            str] = f'{cls.ALL_APARTMENTS_URL}?begin_date={begin_date}&end_date={end_date}&humans={humans}&city_ids[]={city_ids}'

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

    @classmethod
    def __get_redirect_url_for_pay(cls, calendar_event_id: int) -> str:
        # TODO: Сделать страницу с благодарностями
        # TODO: Сделать систему токенов для начисления бонусов после снятия квартиры
        # TODO: подставить новую ссылку после диплоя
        redirect_after_pay: Final[str] = 'https://posutochno-oneday.ru/'
        url_for_redirect_link_prepare: Final[str] = (
            f'https://realtycalendar.ru/widgets/bookings/moneta/event_calendars/{calendar_event_id}/payments/new'
            f'?token={settings.REALTY_CALENDAR_TOKEN}'
            f'&redirect_url={redirect_after_pay}'
        )

        response: Response = requests.get(url_for_redirect_link_prepare)
        if response.status_code == 200:
            response_data: dict = response.json()
            return response_data.get('url', '/')
        else:
            return '/'

    @classmethod
    def get_price_by_date_range_and_guests(
            cls, apartment_id: int, begin_date: str, end_date: str, humans: int
    ) -> dict:
        request_url: Final[str] = (
            f'https://realtycalendar.ru/widgets/bookings/apartments/{apartment_id}/price.json'
            f'?token={settings.REALTY_CALENDAR_TOKEN}'
            f'&humans={humans}'
            f'&begin_date={begin_date}'
            f'&end_date={end_date}'
        )

        response: Response = requests.get(request_url)

        if response.status_code == 200:
            return response.json()
        else:
            raise RealCalendarPriceException()

    @classmethod
    def __convert_date_for_real_calendar(cls, date: str) -> str:
        split_date: Final[list[str]] = date.split('-')
        return f'{split_date[2]}.{split_date[1]}.{split_date[0]}'

    @classmethod
    def __create_note_for_event(cls, humans: int, notes: str, with_pets: Optional[bool]) -> str:
        note_text: str = f"""
        Гостей: {humans}
        Пожелания: {notes}
        С животными: 
        """
        if with_pets:
            note_text += "Да"
        else:
            note_text += "Нет"

        return note_text

    @classmethod
    def create_calendar_event(cls, booking_form_data: dict, apartment_id: int) -> int:
        email = booking_form_data.get('email', 'Почта не указана')
        phone = booking_form_data.get('phone', 'Номер не указан')
        fio = booking_form_data.get('fio', 'ФИО не указано')

        arrival_time = booking_form_data.get('arrival_time')
        departure_time = booking_form_data.get('departure_time')
        begin_date = booking_form_data.get('begin_date')
        end_date = booking_form_data.get('end_date')
        notes = booking_form_data.get('notes')
        adult_guests = booking_form_data.get('adult_guests')
        with_pets = booking_form_data.get("with_pets", None)
        #
        # print(fio, email, phone)
        # print(arrival_time, departure_time)
        # print(begin_date, end_date)
        # print(notes)
        # print(with_pets)

        begin_date: str = cls.__convert_date_for_real_calendar(begin_date)
        end_date: str = cls.__convert_date_for_real_calendar(end_date)

        price_info: Final[dict] = cls.get_price_by_date_range_and_guests(
            apartment_id=apartment_id,
            begin_date=begin_date,
            end_date=end_date,
            humans=adult_guests
        )

        application_note: Final[str] = cls.__create_note_for_event(
            humans=adult_guests,
            notes=notes,
            with_pets=with_pets
        )

        payload_data: Final[dict] = {
            "event_calendar":
                {
                    "terms_of_service": "1",
                    "arrival_time": arrival_time,
                    "begin_date": begin_date,
                    "end_date": end_date,
                    "departure_time": departure_time,
                    "amount": price_info['amount_for_dates_period'],
                    "notes": application_note,
                    "status": 2,
                    "prepayment": price_info['amount_for_pay'],
                },
            "client":
                {
                    "email": email,
                    "phone": phone,
                    "fio": fio
                }
        }

        response = requests.post(
            url=f'https://realtycalendar.ru/widgets/bookings/apartments/{apartment_id}/event_calendars'
                f'?token={settings.REALTY_CALENDAR_TOKEN}',
            json=payload_data,
            headers={
                "Accept": "*/*"
            }
        )
        response_data = response.json()

        return response_data['id']

    @classmethod
    def get_redirect_url_by_event_id(cls, event_id: int) -> str:
        redirect_url: str = cls.__get_redirect_url_for_pay(
            calendar_event_id=event_id
        )
        return redirect_url

    @classmethod
    def create_booking_apartment_event(cls, apartment_id: int, booking_form_data: dict) -> int:
        apartment_for_booking: Apartment = get_object_or_404(Apartment, pk=apartment_id)

        real_calendar_id: int = apartment_for_booking.real_calendar_id
        event_id: int = cls.create_calendar_event(booking_form_data, real_calendar_id)

        return event_id


def get_min_apartments_price(city_id: Optional[str] = None) -> int:
    if not city_id:
        return Apartment.objects.order_by('price').first().price

    city: City = get_object_or_404(City, pk=city_id)
    return Apartment.objects.filter(city=city).order_by('price').first().price


def get_max_apartments_price(city_id: Optional[str] = None) -> int:
    if not city_id:
        return Apartment.objects.order_by('-price').first().price

    city: City = get_object_or_404(City, pk=city_id)
    return Apartment.objects.filter(city=city).order_by('-price').first().price
