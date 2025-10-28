from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class EmailLoginView(LoginView):
    template_name = 'registration/login.html'


class EmailLogoutView(LogoutView):
    next_page = reverse_lazy('home')
