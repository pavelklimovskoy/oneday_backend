from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic import TemplateView

from vacancies.models import Vacancy


class VacanciesView(TemplateView):
    template_name = "vacancies.html"

    def get_context_data(self, **kwargs):
        context = {
            'vacancies': Vacancy.objects.all()
        }
        return context

    def post(self, request, *args, **kwargs):
        subject = f'Заявка на вакансию от  {request.POST['name']} на должность {request.POST['jobs']}'
        message = f'Телефон {request.POST['phone']} Почта {request.POST['email']} вакансия {request.POST['jobs']}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['klimovskoy@sfedu.ru',]

        send_mail(subject, message, email_from, recipient_list)

        return redirect('/')
