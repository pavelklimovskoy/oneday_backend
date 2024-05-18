from django.urls import path

from manual_pages.views import RulesView, CleaningChecklistView, MainPageView

manual_pages = [
    path('cleaning_checklist/', CleaningChecklistView.as_view(), name='cleaning_checklist'),
    path('rules/', RulesView.as_view(), name='rules'),
]

main_page_urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
]
