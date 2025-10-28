from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Account


class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'accounts/list.html'

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user, archived=False)


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['name', 'opening_balance']
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('account_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['name', 'opening_balance', 'archived']
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('account_list')

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'accounts/confirm_delete.html'
    success_url = reverse_lazy('account_list')

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
