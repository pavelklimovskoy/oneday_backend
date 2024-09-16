from django.urls import path

from attractions.views import AttractionView, AllAttractionView

attractions_pages = [
    path('<int:city_id>/', AttractionView.as_view(), name='attractions_view'),
    path('', AllAttractionView.as_view(), name='attractions_view'),
]
