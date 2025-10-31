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
        # Previous month first day (for table carry-over fetch)
        p_year, p_month = sel_year, sel_month - 1
        if p_month == 0:
            p_month = 12
            p_year -= 1
        prev_first_day = date(p_year, p_month, 1)

        # Carry-over base (limitar ao ano corrente)
        base_start = date(sel_year, 1, 1)

        # Onboarding: se informado, não considerar dias anteriores ao onboarding
        onboarding_str = self.request.GET.get('onboarding')
        onboarding_date = None
        if onboarding_str:
            try:
                y, m, d = onboarding_str.split('-')
                onboarding_date = date(int(y), int(m), int(d))
            except Exception:
                onboarding_date = None
        else:
            # fallback para demo conhecida
            if getattr(user, 'email', '').lower() in {'carry@demo.com', '123@gmail.com'}:
                onboarding_date = date(2025, 1, 15)

        effective_start = base_start
        if onboarding_date and onboarding_date.year == sel_year:
            # Respeita o onboarding dentro do ano selecionado
            if onboarding_date > base_start:
                effective_start = onboarding_date

        # Span de meses do effective_start até o mês selecionado (inclusivo)
        months_span = (sel_year - effective_start.year) * 12 + (sel_month - effective_start.month) + 1

        accounts = account_selectors.active_by_user(user)

        # Compute projection from base_start to selected month (ensures carry-over)
        daily = compute_projection(user, effective_start, months=months_span)
        start_str = first_day.strftime('%Y-%m-%d')
        end_str = last_day.strftime('%Y-%m-%d')
        month_days = [d for d in daily if start_str <= d['date'] <= end_str]
        # Previous month end balance for reference
        if sel_month > 1:
            co_year, co_month = sel_year, sel_month - 1
        else:
            co_year, co_month = sel_year - 1, 12
        co_last_day = date(co_year, co_month, calendar.monthrange(co_year, co_month)[1])
        co_last_str = co_last_day.strftime('%Y-%m-%d')
        prev_end_matches = [d for d in daily if d['date'] == co_last_str]
        prev_end_balance = float(prev_end_matches[-1]['saldo']) if prev_end_matches else 0.0
        income = sum(float(d.get('entrada') or 0) for d in month_days)
        expense = sum((float(d.get('saida') or 0) + float(d.get('diario') or 0)) for d in month_days)
        performance = income - expense
        balance = float(month_days[-1]['saldo']) if month_days else 0.0
        ctx.update({
            'base_start': effective_start,
            'span_months': months_span,
            'accounts': accounts,
            'income_total': income,
            'expense_total': expense,
            'performance_total': performance,
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

