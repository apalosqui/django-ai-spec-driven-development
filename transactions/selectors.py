from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from django.db.models import QuerySet

from .models import Transaction


@dataclass(frozen=True)
class TransactionFilters:
    account_id: Optional[int] = None
    category_id: Optional[int] = None
    date_from: Optional[str] = None  # ISO yyyy-mm-dd (kept simple)
    date_to: Optional[str] = None
    query: Optional[str] = None


def for_user(user, filters: Optional[TransactionFilters] = None) -> QuerySet[Transaction]:
    qs: QuerySet[Transaction] = Transaction.objects.filter(account__user=user)
    if not filters:
        return qs

    if filters.account_id:
        qs = qs.filter(account_id=filters.account_id)
    if filters.category_id:
        qs = qs.filter(category_id=filters.category_id)
    if filters.date_from:
        qs = qs.filter(date__gte=filters.date_from)
    if filters.date_to:
        qs = qs.filter(date__lte=filters.date_to)
    if filters.query:
        qs = qs.filter(description__icontains=filters.query)
    return qs


def totals_for_user(user) -> tuple:
    from django.db.models import Sum

    qs = Transaction.objects.filter(account__user=user)
    income = qs.filter(kind='income').aggregate(total=Sum('amount'))['total'] or 0
    expense = qs.filter(kind='expense').aggregate(total=Sum('amount'))['total'] or 0
    return income, expense


def recent_for_user(user, limit: int = 10) -> QuerySet[Transaction]:
    return Transaction.objects.filter(account__user=user).order_by('-date', '-id')[:limit]
