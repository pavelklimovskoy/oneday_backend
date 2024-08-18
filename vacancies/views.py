from django.shortcuts import render
from django.views.generic import TemplateView


class VacanciesView(TemplateView):
    template_name = "vacancies.html"
