from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Case, When, F
from django.views.generic import TemplateView

from accounts.models import Account
from transactions.models import Transaction


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        accounts = Account.objects.filter(user=user, archived=False)
        tx = Transaction.objects.filter(account__user=user)
        income = tx.filter(kind='income').aggregate(total=Sum('amount'))['total'] or 0
        expense = tx.filter(kind='expense').aggregate(total=Sum('amount'))['total'] or 0
        balance_tx = income - expense
        opening_total = accounts.aggregate(total=Sum('opening_balance'))['total'] or 0
        balance = opening_total + balance_tx
        recent = tx.order_by('-date', '-id')[:10]
        ctx.update({
            'accounts': accounts,
            'income_total': income,
            'expense_total': expense,
            'balance': balance,
            'recent_transactions': recent,
        })
        return ctx

