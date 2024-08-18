from django.urls import path

from manual_pages.views import MainPageView

apartments_pages = [
    path('', MainPageView.as_view(), name='search_apartments'),
]
