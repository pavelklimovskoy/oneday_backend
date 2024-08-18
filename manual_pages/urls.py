from django.urls import path

from manual_pages.views import RulesView, CleaningChecklistView, MainPageView, FAQView, KrasnodarView, SochiView, \
    RostovView, TaganrogView, ContactsView

manual_pages = [
    path('cleaning_checklist/', CleaningChecklistView.as_view(), name='cleaning_checklist'),
    path('rules/', RulesView.as_view(), name='rules'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]

main_page_urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
]

attractions_pages = [
    path('krasnodar/', KrasnodarView.as_view(), name='krasnodar'),
    path('rostov/', RostovView.as_view(), name='rostov'),
    path('sochi/', SochiView.as_view(), name='sochi'),
    path('taganrog/', TaganrogView.as_view(), name='taganrog')
]