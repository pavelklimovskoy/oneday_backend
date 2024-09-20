from django.contrib import admin

from user_profile.models import UserProfile, BookingRecord


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(BookingRecord)
class BookingRecordAdmin(admin.ModelAdmin):
    pass
