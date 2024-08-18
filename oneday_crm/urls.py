from django.contrib import admin
from django.urls import path, include

from analytics.views import BookingAnalyticsView
from manual_pages.urls import manual_pages, main_page_urlpatterns, attractions_pages
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
    path("", include(main_page_urlpatterns)),
    path("profile/", include(profile_pages)),
    path("vacancies/", include(vacancies_pages)),
]
