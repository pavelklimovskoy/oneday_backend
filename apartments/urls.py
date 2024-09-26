from django.urls import path

from apartments.views import SearchApartmentsView, ApartmentView, AddToFavoriteView, DeleteFromFavoriteView, \
    SyncApartmentView, BookingApartmentView

apartments_pages = [
    path('synchronize/', SyncApartmentView.as_view(), name='sync_apartments'),
    path('<int:apartment_id>/booking/', BookingApartmentView.as_view(), name='booking_apartment'),
    path('list/', SearchApartmentsView.as_view(), name='search_page'),
    path('<int:apartment_id>/', ApartmentView.as_view(), name='apartment_page'),
    path('<int:apartment_id>/add_to_favorite/', AddToFavoriteView.as_view(), name='add_to_favorite'),
    path('<int:apartment_id>/remove_from_favorite/', DeleteFromFavoriteView.as_view(), name='add_to_favorite'),
]
