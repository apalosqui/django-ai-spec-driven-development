from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Dict, Iterable, List, Tuple

from django.db import transaction

from accounts.models import Account
from cards.models import CardInvoice
from transactions.models import ProjectionSnapshot, Transfer
from .models import FixedExpense, SalaryRule, VariableBudget


def _is_business_day(d: date) -> bool:
    return d.weekday() < 5  # Mon-Fri


def _prev_business_day(d: date) -> date:
    while not _is_business_day(d):
        d = d - timedelta(days=1)
    return d


def _days_in_month(d: date) -> int:
    from calendar import monthrange

    return monthrange(d.year, d.month)[1]


def _parse_days(rule: SalaryRule) -> List[int]:
    if not rule.days:
        return []
    out = []
    for part in rule.days.split(','):
        part = part.strip()
        if not part:
            continue
        try:
            out.append(int(part))
        except Exception:
            continue
    return out


def _daterange(start: date, end: date) -> Iterable[date]:
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


@transaction.atomic
def compute_projection(user, start: date, months: int = 24) -> List[Dict]:
    # Horizon end date
    y = start.year
    m = start.month + months
    y += (m - 1) // 12
    m = (m - 1) % 12 + 1
    from calendar import monthrange

    end = date(y, m, min(start.day, monthrange(y, m)[1]))

    # Initial balances (sum of all accounts)
    opening_total = Account.objects.filter(user=user).aggregate_sum = None
    from django.db.models import Sum
    opening_total = Account.objects.filter(user=user).aggregate(total=Sum('opening_balance'))['total'] or 0
    balance = float(opening_total)

    # Prefetch data
    salary_rules = list(SalaryRule.objects.filter(user=user))
    fixed_expenses = list(FixedExpense.objects.filter(user=user))
    variable_budgets = list(VariableBudget.objects.filter(user=user, active=True))
    invoices_by_due: Dict[date, List[CardInvoice]] = {}
    for inv in CardInvoice.objects.filter(card__user=user, due_date__gte=start, due_date__lte=end):
        invoices_by_due.setdefault(inv.due_date, []).append(inv)
    transfers_by_date: Dict[date, List[Transfer]] = {}
    for tr in Transfer.objects.filter(user=user, date__gte=start, date__lte=end):
        transfers_by_date.setdefault(tr.date, []).append(tr)

    results: List[Dict] = []

    for d in _daterange(start, end):
        entries = 0.0  # receitas do dia (ex.: salários)
        exits = 0.0    # saídas do dia (fixos e boletos/faturas pagas no dia)
        diario = 0.0   # projeção de variável/dia
        events: List[Dict] = []

        # Salaries
        for r in salary_rules:
            hit = False
            days = _parse_days(r)
            if days and d.day in days:
                hit = True
            if r.ultimo_dia_util and d == _prev_business_day(date(d.year, d.month, _days_in_month(d))):
                hit = True
            if hit:
                entries += float(r.amount)
                events.append({'type': 'SALARIO', 'value': float(r.amount)})

        # Fixed expenses
        for fx in fixed_expenses:
            due = date(d.year, d.month, min(fx.due_day, _days_in_month(d)))
            when = _prev_business_day(due) if fx.pay_early_business_day else due
            if d == when:
                exits += float(fx.amount)
                events.append({'type': 'FIXO', 'name': fx.name, 'value': float(fx.amount)})

        # Variable budgets (daily quota) — apenas na coluna "Diário"
        if variable_budgets:
            diario = sum(float(v.monthly_amount) / _days_in_month(d) for v in variable_budgets)
            if diario:
                events.append({'type': 'VARIAVEL', 'value': round(diario, 2)})

        # Invoices due (baixa no vencimento)
        for inv in invoices_by_due.get(d, []):
            exits += float(inv.total_calculated)
            events.append({'type': 'FATURA', 'card': inv.card_id, 'value': float(inv.total_calculated)})

        # Transfers (zero net effect for total saldo; registrar apenas evento)
        for tr in transfers_by_date.get(d, []):
            events.append({'type': 'TRANSFER', 'kind': tr.kind, 'value': float(tr.value)})

        # Saldo = saldo anterior + entradas - saídas - variável/dia
        balance = balance + entries - exits - diario

        # Optional snapshot cache per day
        ProjectionSnapshot.objects.update_or_create(
            user=user, date=d, defaults={'projected_balance': balance, 'meta_info_json': {}}
        )

        results.append({
            'date': d.isoformat(),
            'entrada': round(entries, 2),
            'saida': round(exits, 2),
            'diario': round(diario, 2),
            'saldo': round(balance, 2),
            'eventos': events,
        })

    return results
