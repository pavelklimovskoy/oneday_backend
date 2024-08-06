from django.core.mail import send_mail
from django.views.generic import TemplateView

from manual_pages.models import Rules, CleaningChecklistItem


class CleaningChecklistView(TemplateView):
    template_name = "cleaning_checklist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["checklist_items"] = CleaningChecklistItem.objects.all()
        return context


class RulesView(TemplateView):
    template_name = "rules.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rules"] = Rules.objects.all()
        return context


class MainPageView(TemplateView):
    template_name = "main_page.html"

    def get_context_data(self, **kwargs):

        subject = 'welcome to GFG world'
        message = f'Hi, thank you for registering in geeksforgeeks.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['klimovskoy@sfedu.ru', ]
        send_mail(subject, message, email_from, recipient_list)

        context = super().get_context_data(**kwargs)
        return context


class FAQView(TemplateView):
    template_name = "faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faq"] = Faq.objects.all()
        return context


class KrasnodarView(TemplateView):
    template_name = "attractions_krasnodar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
