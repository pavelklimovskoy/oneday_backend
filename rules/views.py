from django.http import HttpResponse
from django.views.generic import TemplateView

from cleaning_checklist.models import CleaningChecklistItem
from rules.models import Rules


class RulesView(TemplateView):
    template_name = "rules.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rules"] = Rules.objects.all()
        return context
