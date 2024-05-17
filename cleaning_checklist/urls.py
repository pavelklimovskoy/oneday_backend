from django.urls import path

from cleaning_checklist.views import CleaningChecklistView

checklist_urlpatterns = [
    path('', CleaningChecklistView.as_view(), name='cleaning_checklist'),
]
