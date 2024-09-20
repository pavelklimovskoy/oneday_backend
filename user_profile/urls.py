from django.contrib.auth.views import LogoutView
from django.urls import path

from user_profile.views import ProfileView, FavoritesView, HistoryView, ProfileLoginView, DeleteProfileAvatarView, \
    UploadProfileAvatarView, UpdateProfileInfoView

profile_pages = [
    path('edit/', ProfileView.as_view(), name='edit_profile'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('history/', HistoryView.as_view(), name='history'),
    path('login/', ProfileLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete_avatar/', DeleteProfileAvatarView.as_view(), name='delete_avatar'),
    path('upload_avatar/', UploadProfileAvatarView.as_view(), name='upload_avatar'),
    path('update_profile_info/', UpdateProfileInfoView.as_view(), name='upload_avatar'),
]
