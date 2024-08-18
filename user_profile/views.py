from django.shortcuts import render
from django.views.generic import TemplateView


class ProfileView(TemplateView):
    template_name = 'profile.html'


class FavoritesView(TemplateView):
    template_name = 'favorites_apartments.html'


class HistoryView(TemplateView):
    template_name = 'booking_history.html'
