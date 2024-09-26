from typing import Final, TypeAlias

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from django.db.models import Min, Max
from django.http import JsonResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from rest_framework.request import Request
from rest_framework.views import APIView

from apartments.models import Apartment, City
from apartments.uttils import RealtyCalendar, get_max_apartments_price, get_min_apartments_price
from manual_pages.views import TemplateView
from user_profile.models import UserProfile

RedirectType: TypeAlias = HttpResponsePermanentRedirect | HttpResponseRedirect


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
            # RealtyCalendar.download_apartments_info()
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
            context['min_apartment_price'] = get_min_apartments_price()
            context['max_apartment_price'] = get_max_apartments_price()
            return context

        city = get_object_or_404(City, pk=city_id)

        context["apartments"] = Apartment.objects.filter(city=city)
        context['min_apartment_price'] = get_min_apartments_price(city_id)
        context['max_apartment_price'] = get_max_apartments_price(city_id)
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
        with transaction.atomic():
            try:
                user = get_object_or_404(UserProfile, pk=request.user.id)
                apartment = get_object_or_404(Apartment, pk=apartment_id)
                user.favorites_apartments.add(apartment)
            except Exception as e:
                raise e

        return redirect("/".join(request.path.split('/')[:-2]))


class DeleteFromFavoriteView(View):
    def get(self, request: WSGIRequest, apartment_id: int, *args, **kwargs) -> RedirectType:
        with transaction.atomic():
            try:
                user = get_object_or_404(UserProfile, pk=request.user.id)
                apartment = get_object_or_404(Apartment, pk=apartment_id)
                user.favorites_apartments.remove(apartment)
            except Exception as e:
                raise e

        return redirect('/profile/favorites/')


class BookingApartmentView(APIView):
    def post(self, request: Request, apartment_id: int, *args, **kwargs) -> RedirectType:
        booking_event_id: Final[int] = RealtyCalendar.create_booking_apartment_event(
            apartment_id=apartment_id,
            booking_form_data=request.data
        )

        redirect_url: Final[str] = RealtyCalendar.get_redirect_url_by_event_id(
            event_id=booking_event_id,
        )

        return redirect(redirect_url)
