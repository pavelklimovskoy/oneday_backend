from django.db.models import Min, Max
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from apartments.models import Apartment, City
from apartments.uttils import RealtyCalendar


def get_min_apartments_price_for_city(city_id: str) -> int:
    city = City.objects.get(pk=city_id)
    return Apartment.objects.filter(city=city).aggregate(min_price=Min('price'))['min_price']


def get_max_apartments_price_for_city(city_id: str) -> int:
    city = City.objects.get(pk=city_id)
    return Apartment.objects.filter(city=city).aggregate(min_price=Max('price'))['min_price']


class SearchApartmentsView(TemplateView):
    template_name = 'apartments_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # RealtyCalendar.download_apartments_info()

        city_id = self.request.GET.get('city', 'undefined')
        city = get_object_or_404(City, pk=city_id)

        context["apartments"] = Apartment.objects.filter(city=city)

        context['min_apartment_price'] = get_min_apartments_price_for_city(city_id)
        context['max_apartment_price'] = get_max_apartments_price_for_city(city_id)

        context['city_longitude'] = city.map_longitude
        context['city_latitude'] = city.map_latitude
        context['map_view_zoom'] = city.map_view_zoom

        return context


class ApartmentView(TemplateView):
    template_name = 'apartment_page.html'

    def get_context_data(self, apartment_id, **kwargs):
        context = super().get_context_data(**kwargs)

        get_object_or_404(Apartment, pk=apartment_id)

        context['apartment'] = Apartment.objects.get(pk=apartment_id)

        return context
