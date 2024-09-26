from django import forms

from user_profile.models import UserProfile


class UpdateAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', ]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'email', 'first_name', 'last_name', 'gender', 'telegram_nickname']
