from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Dict, Iterable, List, Tuple

from django.db import transaction

from accounts.models import Account
from cards.models import CardInvoice
from transactions.models import ProjectionSnapshot, Transfer, Transaction as Tx
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


def compute_projection(user, start: date, months: int = 24) -> List[Dict]:
    # Horizon end date: include full months.
    # Example: start=2025-09-01, months=2 -> cover 2025-09-01 .. 2025-10-31
    from calendar import monthrange
    if months < 1:
        months = 1
    idx = (start.month - 1) + (months - 1)
    end_year = start.year + (idx // 12)
    end_month = (idx % 12) + 1
    end_day = monthrange(end_year, end_month)[1]
    end = date(end_year, end_month, end_day)

    # Initial balances (sum of all accounts)
    from django.db.models import Sum
    opening_total = Account.objects.filter(user=user).aggregate(total=Sum('opening_balance'))['total'] or 0
    balance = float(opening_total)

    # Prefetch data
    salary_rules = list(SalaryRule.objects.filter(user=user))
    fixed_expenses = list(FixedExpense.objects.filter(user=user))
    variable_budgets = list(VariableBudget.objects.filter(user=user, active=True))

    # Debug logging
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f'[Projection] User {user.id}: start={start}, months={months}, end={end}')
    logger.info(f'[Projection] User {user.id}: salary_rules={len(salary_rules)}, fixed_expenses={len(fixed_expenses)}, variable_budgets={len(variable_budgets)}, opening_total={opening_total}')
    if salary_rules:
        logger.info(f'[Projection] Salary rules detail: {[(r.amount, r.days, r.ultimo_dia_util) for r in salary_rules]}')
    if fixed_expenses:
        logger.info(f'[Projection] Fixed expenses detail: {[(f.name, f.amount, f.due_day) for f in fixed_expenses]}')
    if variable_budgets:
        logger.info(f'[Projection] Variable budgets detail: {[(v.category, v.monthly_amount) for v in variable_budgets]}')
    invoices_by_due: Dict[date, List[CardInvoice]] = {}
    for inv in CardInvoice.objects.filter(card__user=user, due_date__gte=start, due_date__lte=end):
        invoices_by_due.setdefault(inv.due_date, []).append(inv)
    transfers_by_date: Dict[date, List[Transfer]] = {}
    for tr in Transfer.objects.filter(user=user, date__gte=start, date__lte=end):
        transfers_by_date.setdefault(tr.date, []).append(tr)

    # One-off transactions (income/expense)
    # Separar despesas diárias (marcadas com [DIARIO]) de despesas fixas pontuais
    incomes_by_date: Dict[date, float] = {}
    daily_expenses_by_date: Dict[date, float] = {}  # vai para coluna "Diário"
    fixed_expenses_by_date: Dict[date, float] = {}  # vai para coluna "Saída"
    for t in Tx.objects.filter(account__user=user, date__gte=start, date__lte=end):
        if t.kind == 'income':
            incomes_by_date[t.date] = incomes_by_date.get(t.date, 0.0) + float(t.amount)
        else:
            # Expense: verificar se é diária (marcador [DIARIO]) ou fixa pontual
            if t.description and t.description.startswith('[DIARIO]'):
                daily_expenses_by_date[t.date] = daily_expenses_by_date.get(t.date, 0.0) + float(t.amount)
            else:
                fixed_expenses_by_date[t.date] = fixed_expenses_by_date.get(t.date, 0.0) + float(t.amount)

    results: List[Dict] = []

    for d in _daterange(start, end):
        entries = 0.0  # receitas do dia (ex.: salários)
        exits = 0.0    # saídas do dia (fixos e boletos/faturas pagas no dia)
        diario = 0.0   # projeção de variável/dia
        events: List[Dict] = []

        # Salaries (rules)
        for r in salary_rules:
            try:
                created_limit = r.created_at.date()
            except Exception:
                created_limit = start
            if d < created_limit:
                continue
            hit = False
            days = _parse_days(r)
            if days and d.day in days:
                hit = True
            if r.ultimo_dia_util and d == _prev_business_day(date(d.year, d.month, _days_in_month(d))):
                hit = True
            if hit:
                entries += float(r.amount)
                events.append({'type': 'SALARIO', 'value': float(r.amount)})

        # Fixed expenses (recurring)
        for fx in fixed_expenses:
            try:
                created_limit = fx.created_at.date()
            except Exception:
                created_limit = start
            if d < created_limit:
                continue
            due = date(d.year, d.month, min(fx.due_day, _days_in_month(d)))
            when = _prev_business_day(due) if fx.pay_early_business_day else due
            if d == when:
                exits += float(fx.amount)
                events.append({'type': 'FIXO', 'name': fx.name, 'value': float(fx.amount)})

        # Variable budgets (daily quota) - calculate but don't add event yet
        if variable_budgets:
            diario = 0.0
            for v in variable_budgets:
                try:
                    created_limit = v.created_at.date()
                except Exception:
                    created_limit = start
                if d < created_limit:
                    continue
                diario += float(v.monthly_amount) / _days_in_month(d)

        # One-off transactions on date d
        if d in incomes_by_date:
            entries += incomes_by_date[d]
            events.append({'type': 'RECEITA', 'value': incomes_by_date[d]})

        # Despesas fixas pontuais (Transaction sem marcador [DIARIO]) -> coluna "Saída"
        if d in fixed_expenses_by_date:
            exits += fixed_expenses_by_date[d]
            events.append({'type': 'DESPESA', 'value': fixed_expenses_by_date[d]})

        # Despesas diárias (Transaction com marcador [DIARIO]) -> coluna "Diário" (substitui variável)
        if d in daily_expenses_by_date:
            diario = daily_expenses_by_date[d]
            events.append({'type': 'DESPESA_DIARIA', 'value': daily_expenses_by_date[d]})
        elif diario > 0:
            # Se não há despesa diária, mostra o valor variável diluído
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
