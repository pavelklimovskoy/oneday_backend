from django import forms
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apartments.models import Apartment
from manual_pages.views import TemplateView
from user_profile.forms import UpdateAvatarForm, UserProfileForm
from user_profile.models import UserProfile, BookingRecord


class RedirectLoginRequiredMixin(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'redirect_to'


class ProfileView(RedirectLoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'


class FavoritesView(RedirectLoginRequiredMixin, TemplateView):
    template_name = 'profile/favorites_apartments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.request.user.id
        user = get_object_or_404(UserProfile, pk=user_id)

        context["apartments"] = user.favorites_apartments.all()

        return context


class HistoryView(RedirectLoginRequiredMixin, TemplateView):
    template_name = 'profile/booking_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #
        # user_id = self.request.user.id
        # user = get_object_or_404(UserProfile, pk=user_id)
        #
        # context["booking_history"] = BookingRecord.objects.filter(user_profile=user).order_by('-start_date')

        return context


class ProfileAuthenticationForm(AuthenticationForm):
    redirect_url = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'username__input'}
        self.fields['password'].widget.attrs = {'class': 'password__input'}

        self.fields['username'].label_suffix = ''
        self.fields['password'].label_suffix = ''

        self.fields['redirect_url'].widget = self.fields['redirect_url'].hidden_widget()


class ProfileLoginView(LoginView):
    form_class = ProfileAuthenticationForm

    redirect_authenticated_user = True

    def get_success_url(self):
        super().get_success_url()
        return f'/profile/edit/'

    def form_invalid(self, form):
        context = self.get_context_data(**form.cleaned_data)

        messages.error(self.request, message="Неверный логин или пароль")

        return redirect(form.cleaned_data['redirect_url'])


class DeleteProfileAvatarView(RedirectLoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        if not user_id:
            return redirect('/profile/edit/')

        UserProfile.objects.get(pk=user_id).profile_picture.delete()

        return redirect('/profile/edit/')


class UploadProfileAvatarView(RedirectLoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        user_id = request.user.id

        if not user_id:
            return redirect('/profile/edit/')

        user = get_object_or_404(UserProfile, id=user_id)
        form = UpdateAvatarForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(self.request, message="Данные успешно обновлены")
            return redirect('/profile/edit/')

        return redirect('/profile/edit/')


class UpdateProfileInfoView(RedirectLoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        user_id = request.user.id

        if not user_id:
            return redirect('/profile/edit/')

        user = get_object_or_404(UserProfile, id=user_id)
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/profile/edit/')

        return redirect('/profile/edit/')
