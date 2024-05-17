from django.views.generic import TemplateView

from cleaning_checklist.models import CleaningChecklistItem


class CleaningChecklistView(TemplateView):
    template_name = "cleaning_checklist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["checklist_items"] = CleaningChecklistItem.objects.all()
        return context
