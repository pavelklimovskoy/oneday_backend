from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
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
        recipient_list = ['klimovskoy@sfedu.ru', 'sempereksenia@gmail.com']

        vacancy = Vacancy.objects.get(pk=request.POST['jobs'])
        vacancy_title = vacancy.title
        vacancy_salary = vacancy.salary
        vacancy_description = vacancy.description
        vacancy_address = vacancy.address

        email_context = {
            'message': message,
            'vacancies_name': request.POST['jobs'],
            'user_name': request.POST['name'],
            'contact_email': request.POST['email'],
            'phone': request.POST['phone'],
            'vacancy_title': vacancy_title,
            'vacancy_salary': vacancy_salary,
            'vacancy_description': vacancy_description,
            'vacancy_address': vacancy_address
        }
        html_message = render_to_string('email_vacancie_template.html', email_context)

        send_mail(
            subject,
            '',
            email_from,
            recipient_list,
            html_message=html_message,
        )

        return redirect('/')
