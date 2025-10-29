from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Transaction
from accounts.models import Account
from categories.models import Category
from accounts import selectors as account_selectors
from categories import selectors as category_selectors
from . import selectors as tx_selectors


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/list.html'

    def get_queryset(self):
        filters = tx_selectors.TransactionFilters(
            account_id=self._to_int(self.request.GET.get('account')),
            category_id=self._to_int(self.request.GET.get('category')),
            date_from=self.request.GET.get('date_from') or None,
            date_to=self.request.GET.get('date_to') or None,
            query=self.request.GET.get('q') or None,
        )
        return tx_selectors.for_user(self.request.user, filters)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['accounts'] = account_selectors.by_user(self.request.user)
        ctx['categories'] = category_selectors.by_user(self.request.user)
        return ctx


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['account', 'category', 'kind', 'amount', 'date', 'description']
    template_name = 'transactions/form.html'
    success_url = reverse_lazy('transaction_list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['account'].queryset = account_selectors.by_user(self.request.user)
        form.fields['category'].queryset = category_selectors.by_user(self.request.user)
        return form

    @staticmethod
    def _to_int(value):
        try:
            return int(value) if value not in (None, '') else None
        except (TypeError, ValueError):
            return None


class TransactionUpdateView(TransactionCreateView, UpdateView):
    success_url = reverse_lazy('transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(account__user=self.request.user)


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/confirm_delete.html'
    success_url = reverse_lazy('transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(account__user=self.request.user)
