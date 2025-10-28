from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .forms import ProfileForm


class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'profiles/detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'profiles/form.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profiles:detail')
    success_message = 'Perfil atualizado com sucesso.'

    def get_object(self, queryset=None):
        return self.request.user.profile
