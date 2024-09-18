from django.views.generic import TemplateView

from manual_pages.models import Rules, CleaningChecklistItem, Faq


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
        context = super().get_context_data(**kwargs)
        return context


class ContactsView(TemplateView):
    template_name = "contacts.html"


class FAQView(TemplateView):
    template_name = "faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faq"] = Faq.objects.all()
        return context
