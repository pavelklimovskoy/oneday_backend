from typing import Final

import requests
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Min, Max
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from requests import Response

from apartments.models import Apartment, City
from apartments.uttils import RealtyCalendar
from manual_pages.views import TemplateView
from user_profile.models import UserProfile


def get_min_price_from_apartments() -> int:
    return Apartment.objects.order_by('price').first().price


def get_max_price_from_apartments() -> int:
    return Apartment.objects.order_by('-price').first().price


def get_min_apartments_price_for_city(city_id: str) -> int:
    city = City.objects.get(pk=city_id)
    return Apartment.objects.filter(city=city).aggregate(min_price=Min('price'))['min_price']


def get_max_apartments_price_for_city(city_id: str) -> int:
    city = City.objects.get(pk=city_id)
    return Apartment.objects.filter(city=city).aggregate(min_price=Max('price'))['min_price']


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class SyncApartmentView(View, SuperuserRequiredMixin):
    def get(self, *args, **kwargs):
        new_added_apartments = RealtyCalendar.download_apartments_info()

        return JsonResponse(
            data={
                'new_added_apartments': new_added_apartments
            },
            status=200
        )


class SearchApartmentsView(TemplateView):
    template_name = 'apartment/apartments_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        city_id: str | None = self.request.GET.get('city', None)
        arrival: str | None = self.request.GET.get('arrival', None)
        departure: str | None = self.request.GET.get('departure', None)
        guests_counts: int | None = self.request.GET.get('guests_counts', None)

        if not arrival and not departure and not city_id:
            RealtyCalendar.download_apartments_info()
            context['city_title'] = 'Все города'
            context['city_longitude'] = '22'
            context['city_latitude'] = '23'
            context['map_view_zoom'] = '15'
            context['arrival'] = "Дата заезда"
            context['departure'] = "Дата выезда"

            apartments_to_context = None
            if not guests_counts:
                apartments_to_context = Apartment.objects.all()
            else:
                apartments_to_context = Apartment.objects.filter(humans__lte=guests_counts)

            context['apartments'] = apartments_to_context
            context['min_apartment_price'] = apartments_to_context.aggregate(min_price=Min('price'))['min_price']
            context['max_apartment_price'] = apartments_to_context.aggregate(min_price=Max('price'))['min_price']

            return context

        if arrival and departure and city_id:
            city = get_object_or_404(City, pk=city_id)

            apartments_ids = RealtyCalendar.get_apartments_in_date_range(
                begin_date=arrival,
                end_date=departure,
                city_ids=city_id,
                humans=guests_counts
            )

            context['city_title'] = city.title
            context['city_longitude'] = city.map_longitude
            context['city_latitude'] = city.map_latitude
            context['map_view_zoom'] = city.map_view_zoom
            context['arrival'] = "Дата заезда"
            context['departure'] = "Дата выезда"

            apartments_to_context = None
            if not guests_counts:
                apartments_to_context = Apartment.objects.all()
            else:
                apartments_to_context = Apartment.objects.filter(humans__lte=guests_counts)

            context['apartments'] = apartments_to_context
            context['min_apartment_price'] = apartments_to_context.aggregate(min_price=Min('price'))['min_price']
            context['max_apartment_price'] = apartments_to_context.aggregate(min_price=Max('price'))['min_price']

            return context
        elif arrival and departure:
            RealtyCalendar.get_apartments_in_date_range(
                begin_date=arrival,
                end_date=departure,
                humans=guests_counts
            )
        elif not arrival and not departure and not city_id:
            RealtyCalendar.download_apartments_info()

        if city_id == 'undefined':
            context["apartments"] = Apartment.objects.all()
            context['min_apartment_price'] = get_min_price_from_apartments()
            context['max_apartment_price'] = get_max_price_from_apartments()
            return context

        city = get_object_or_404(City, pk=city_id)

        context["apartments"] = Apartment.objects.filter(city=city)

        context['min_apartment_price'] = get_min_apartments_price_for_city(city_id)
        context['max_apartment_price'] = get_max_apartments_price_for_city(city_id)

        context['city_title'] = city.title
        context['city_longitude'] = city.map_longitude
        context['city_latitude'] = city.map_latitude
        context['map_view_zoom'] = city.map_view_zoom

        context['arrival'] = arrival
        context['departure'] = departure

        return context


class ApartmentView(TemplateView):
    template_name = 'apartment/apartment_page.html'

    def get_context_data(self, apartment_id, **kwargs):
        context = super().get_context_data(**kwargs)

        apartment = get_object_or_404(Apartment, pk=apartment_id)

        context['apartment'] = apartment
        context['description'] = apartment.desc.replace('<br>', '')
        context['sleep_types'] = apartment.sleeps.split('+')

        return context


class AddToFavoriteView(View):
    def get(self, request, apartment_id, *args, **kwargs):
        user = get_object_or_404(UserProfile, pk=request.user.id)
        apartment = get_object_or_404(Apartment, pk=apartment_id)
        user.favorites_apartments.add(apartment)

        return redirect("/".join(request.path.split('/')[:-2]))


class DeleteFromFavoriteView(View):
    def get(self, request, apartment_id, *args, **kwargs):
        user = get_object_or_404(UserProfile, pk=request.user.id)
        apartment = get_object_or_404(Apartment, pk=apartment_id)
        user.favorites_apartments.remove(apartment)

        return redirect('/profile/favorites/')


class BookingApartmentView(View):

    def get_redirect_url_for_pay(self, calendar_event) -> str:
        redirect_after_pay: Final[str] = 'https://posutochno-oneday.ru/krasnodar/'
        url_for_redirect_link_prepare: Final[str] = (
            f'https://realtycalendar.ru/widgets/bookings/moneta/event_calendars/{calendar_event}/payments/new'
            f'?token=29f9b591c704f9a65bf43ecca4cb2093'
            f'&redirect_url={redirect_after_pay}'
        )

        response = requests.get(url_for_redirect_link_prepare)
        response_data = response.json()

        return response_data.get('url', '/')

    def get_price_by_date_range_and_guests(
            self, apartment_id: int, date_start: str, date_end: str, guests_count: int
    ) -> dict:
        request_url: Final[str] = (
            f'https://realtycalendar.ru/widgets/bookings/apartments/{apartment_id}/price.json'
            f'?token=29f9b591c704f9a65bf43ecca4cb2093'
            f'&humans={guests_count}'
            f'&begin_date={date_start}'
            f'&end_date={date_end}'
        )

        response = requests.get(request_url)
        return response.json()

    def create_calendar_event(self, request, apartment_id) -> int:
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        fio = request.POST.get('fio')

        arrival_time = request.POST.get('arrival_time')
        departure_time = request.POST.get('departure_time')

        begin_date = request.POST.get('begin_date')
        end_date = request.POST.get('end_date')

        notes = request.POST.get('notes')

        adult_guests = request.POST.get('adult-guests')

        print(fio, email, phone)
        print(arrival_time, departure_time)
        print(begin_date, end_date)

        split_date = begin_date.split('-')
        begin_date = f'{split_date[2]}.{split_date[1]}.{split_date[0]}'

        split_date = end_date.split('-')
        end_date = f'{split_date[2]}.{split_date[1]}.{split_date[0]}'

        price_info: dict = self.get_price_by_date_range_and_guests(
            apartment_id=apartment_id,
            date_start=begin_date,
            date_end=end_date,
            guests_count=adult_guests
        )

        payload_data = {
            "event_calendar":
                {
                    "terms_of_service": "1",
                    "arrival_time": arrival_time,
                    "begin_date": begin_date,
                    "end_date": end_date,
                    "departure_time": departure_time,
                    "amount": price_info['amount_for_dates_period'],
                    "notes": f"\nГостей: {adult_guests} \nПожелания:{notes}",
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
            url=f'https://realtycalendar.ru/widgets/bookings/apartments/{apartment_id}/event_calendars?token=29f9b591c704f9a65bf43ecca4cb2093',
            json=payload_data,
            headers={
                "Accept": "*/*"
            }
        )
        response_data = response.json()

        return response_data['id']

    def post(self, request, apartment_id, *args, **kwargs):
        real_calendar_id = Apartment.objects.get(pk=apartment_id).real_calendar_id
        event_id = self.create_calendar_event(request, real_calendar_id)

        redirect_url = self.get_redirect_url_for_pay(
            calendar_event=event_id
        )

        return redirect(redirect_url)
