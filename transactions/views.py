from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Transaction
from accounts.models import Account
from categories.models import Category


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/list.html'

    def get_queryset(self):
        qs = Transaction.objects.filter(account__user=self.request.user)
        account = self.request.GET.get('account')
        category = self.request.GET.get('category')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        q = self.request.GET.get('q')
        if account:
            qs = qs.filter(account_id=account)
        if category:
            qs = qs.filter(category_id=category)
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        if q:
            qs = qs.filter(description__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['accounts'] = Account.objects.filter(user=self.request.user)
        ctx['categories'] = Category.objects.filter(user=self.request.user)
        return ctx


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['account', 'category', 'kind', 'amount', 'date', 'description']
    template_name = 'transactions/form.html'
    success_url = reverse_lazy('transaction_list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['account'].queryset = Account.objects.filter(user=self.request.user)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        return form


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
