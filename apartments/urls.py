from django.urls import path

from apartments.views import SearchApartmentsView, ApartmentView

apartments_pages = [
    path('list/', SearchApartmentsView.as_view(), name='search_page'),
    path('<int:apartment_id>/', ApartmentView.as_view(), name='apartment_page'),
]
