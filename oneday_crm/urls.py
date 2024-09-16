from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from analytics.views import BookingAnalyticsView
from apartments.urls import apartments_pages
from attractions.urls import attractions_pages
from manual_pages.urls import manual_pages
from manual_pages.views import MainPageView
from user_profile.urls import profile_pages
from vacancies.urls import vacancies_pages

admin.site.site_header = 'Oneday CRM'
admin.site.site_title = 'Oneday CRM'
admin.site.index_title = 'Oneday CRM'

urlpatterns = [
    path('oneday_crm/', admin.site.urls),
    path("common/", include(manual_pages)),
    path('attractions/', include(attractions_pages)),
    path("booking_analytics/", BookingAnalyticsView.as_view()),
    path('appartments/', include(apartments_pages)),
    path("profile/", include(profile_pages)),
    path("vacancies/", include(vacancies_pages)),
    path('', MainPageView.as_view(), name='main_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
