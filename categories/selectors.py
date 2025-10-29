from __future__ import annotations

from django.db.models import QuerySet

from .models import Category


def by_user(user) -> QuerySet[Category]:
    return Category.objects.filter(user=user)

