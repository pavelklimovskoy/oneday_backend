"""
URL configuration for oneday_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from analytics.views import BookingAnalyticsView
from manual_pages.urls import manual_pages, main_page_urlpatterns

admin.site.site_header = 'Oneday CRM'
admin.site.site_title = 'Oneday CRM'
admin.site.index_title = 'Oneday CRM'

urlpatterns = [
    path('oneday_crm/', admin.site.urls),
    path("common/", include(manual_pages)),
    path("booking_analytics/", BookingAnalyticsView.as_view()),
    path("", include(main_page_urlpatterns)),
]
