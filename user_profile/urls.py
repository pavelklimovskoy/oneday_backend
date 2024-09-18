from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from user_profile.views import ProfileView, FavoritesView, HistoryView, ProfileLoginView

profile_pages = [
    path('edit/', ProfileView.as_view(), name='edit_profile'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('history/', HistoryView.as_view(), name='history'),
    path('login/', ProfileLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
