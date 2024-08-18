from django.urls import path

from vacancies.views import VacanciesView

vacancies_pages = [
    path('', VacanciesView.as_view(), name='vacancies_list'),
]
