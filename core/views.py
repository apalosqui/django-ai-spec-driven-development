from datetime import date
import calendar

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import TemplateView

from accounts import selectors as account_selectors
from transactions import selectors as tx_selectors
from transactions.models import Transaction
from planning.services import compute_projection


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
        prev_year = sel_year
        prev_month = sel_month - 1
        if prev_month == 0:
            prev_month = 12
            prev_year -= 1
        prev_first_day = date(prev_year, prev_month, 1)

        accounts = account_selectors.active_by_user(user)

        # Compute via projection carrying previous month's balance
        daily = compute_projection(user, prev_first_day, months=2)
        start_str = first_day.strftime('%Y-%m-%d')
        end_str = last_day.strftime('%Y-%m-%d')
        month_days = [d for d in daily if start_str <= d['date'] <= end_str]
        income = sum(float(d.get('entrada') or 0) for d in month_days)
        expense = sum((float(d.get('saida') or 0) + float(d.get('diario') or 0)) for d in month_days)
        balance = float(month_days[-1]['saldo']) if month_days else 0.0
        ctx.update({
            'accounts': accounts,
            'income_total': income,
            'expense_total': expense,
            'balance': balance,
            'selected_month': sel_month,
            'selected_year': sel_year,
            'first_day': first_day,
            'last_day': last_day,
            'prev_first_day': prev_first_day,
            'months': list(range(1, 13)),
            'years': [sel_year - 1, sel_year, sel_year + 1],
        })
        return ctx
