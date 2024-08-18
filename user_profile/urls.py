from django.urls import path

from user_profile.views import ProfileView, FavoritesView, HistoryView

profile_pages = [
    path('edit/', ProfileView.as_view(), name='edit_profile'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('history/', HistoryView.as_view(), name='history'),
]
