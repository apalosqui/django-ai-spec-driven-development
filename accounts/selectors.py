from __future__ import annotations

from django.db.models import QuerySet

from .models import Account


def by_user(user) -> QuerySet[Account]:
    return Account.objects.filter(user=user)


def active_by_user(user) -> QuerySet[Account]:
    return by_user(user).filter(archived=False)

