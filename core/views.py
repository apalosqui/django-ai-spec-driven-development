from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import TemplateView

from accounts import selectors as account_selectors
from transactions import selectors as tx_selectors


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        accounts = account_selectors.active_by_user(user)
        income, expense = tx_selectors.totals_for_user(user)
        balance_tx = income - expense
        opening_total = accounts.aggregate(total=Sum('opening_balance'))['total'] or 0
        balance = opening_total + balance_tx
        recent = tx_selectors.recent_for_user(user, limit=10)
        ctx.update({
            'accounts': accounts,
            'income_total': income,
            'expense_total': expense,
            'balance': balance,
            'recent_transactions': recent,
        })
        return ctx
