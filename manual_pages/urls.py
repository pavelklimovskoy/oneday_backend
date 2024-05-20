from django.urls import path

from manual_pages.views import RulesView, CleaningChecklistView, MainPageView, FAQView, KrasnodarView

manual_pages = [
    path('cleaning_checklist/', CleaningChecklistView.as_view(), name='cleaning_checklist'),
    path('rules/', RulesView.as_view(), name='rules'),
    path('faq/', FAQView.as_view(), name='faq'),
]

main_page_urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
]

attractions_pages = [
    path('krasnodar/', KrasnodarView.as_view(), name='krasnodar'),
    path('rostov/', KrasnodarView.as_view(), name='rostov'),
    path('sochi/', KrasnodarView.as_view(), name='sochi'),
    path('taganrog/', KrasnodarView.as_view(), name='taganrog')
]