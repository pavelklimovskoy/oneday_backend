from django.urls import path

from rules.views import RulesView

rules_urlpatterns = [
    path('', RulesView.as_view(), name='rules'),
]
