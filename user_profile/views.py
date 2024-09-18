from django import forms
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views import View

from manual_pages.views import TemplateView


class RedirectLoginRequiredMixin(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'redirect_to'


class ProfileView(RedirectLoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


class FavoritesView(RedirectLoginRequiredMixin, TemplateView):
    template_name = 'favorites_apartments.html'


class HistoryView(RedirectLoginRequiredMixin, TemplateView):
    template_name = 'booking_history.html'


class ProfileAuthenticationForm(AuthenticationForm):
    redirect_url = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'username__input'}
        self.fields['password'].widget.attrs = {'class': 'password__input'}

        self.fields['username'].label_suffix = ''
        self.fields['password'].label_suffix = ''


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
