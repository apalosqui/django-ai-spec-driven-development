from datetime import date
import calendar

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import TemplateView

from accounts import selectors as account_selectors
from transactions import selectors as tx_selectors
from transactions.models import Transaction


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        # Selected month/year (defaults to current month)
        try:
            sel_month = int(self.request.GET.get('month') or 0)
        except Exception:
            sel_month = 0
        try:
            sel_year = int(self.request.GET.get('year') or 0)
        except Exception:
            sel_year = 0
        today = date.today()
        if not (1 <= sel_month <= 12):
            sel_month = today.month
        if sel_year <= 0:
            sel_year = today.year

        first_day = date(sel_year, sel_month, 1)
        last_day = date(sel_year, sel_month, calendar.monthrange(sel_year, sel_month)[1])

        accounts = account_selectors.active_by_user(user)

        # Totals only for selected month
        month_qs = Transaction.objects.filter(account__user=user, date__gte=first_day, date__lte=last_day)
        income = month_qs.filter(kind='income').aggregate(total=Sum('amount'))['total'] or 0
        expense = month_qs.filter(kind='expense').aggregate(total=Sum('amount'))['total'] or 0

        # Balance approximation: opening balances + net of all transactions up to end of selected month
        # (simplified; dashboard focus)
        all_tx_qs = Transaction.objects.filter(account__user=user, date__lte=last_day)
        total_income_all = all_tx_qs.filter(kind='income').aggregate(total=Sum('amount'))['total'] or 0
        total_expense_all = all_tx_qs.filter(kind='expense').aggregate(total=Sum('amount'))['total'] or 0
        opening_total = accounts.aggregate(total=Sum('opening_balance'))['total'] or 0
        balance = opening_total + (total_income_all - total_expense_all)

        recent = month_qs.order_by('-date', '-id')[:10]
        ctx.update({
            'accounts': accounts,
            'income_total': income,
            'expense_total': expense,
            'balance': balance,
            'recent_transactions': recent,
            'selected_month': sel_month,
            'selected_year': sel_year,
            'first_day': first_day,
            'last_day': last_day,
        })
        return ctx
