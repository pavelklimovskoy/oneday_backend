from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from apartments.models import City
from attractions.models import Attraction


class AttractionView(TemplateView):
    template_name = 'attractions.html'

    def get_context_data(self, city_id, **kwargs):
        context = super().get_context_data(**kwargs)

        get_object_or_404(City, pk=city_id)

        city_name = City.objects.get(pk=city_id).title
        context['city_name'] = city_name

        context['attractions'] = Attraction.objects.filter(city=city_id)

        return context


class AllAttractionView(TemplateView):
    template_name = 'attractions_and_events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['attractions'] = Attraction.objects.all()

        return context
