from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable, List, Optional, Tuple

from django.db import transaction

from .models import CardInvoice, CardTransaction, CreditCard


def _add_month(year: int, month: int, months: int = 1) -> Tuple[int, int]:
    m = month - 1 + months
    y = year + m // 12
    mm = m % 12 + 1
    return y, mm


def _closing_date(year: int, month: int, closing_day: int) -> date:
    # Clamp day to valid range in that month
    from calendar import monthrange

    last = monthrange(year, month)[1]
    day = min(max(1, closing_day), last)
    return date(year, month, day)


def _cycle_range(year: int, month: int, closing_day: int) -> Tuple[date, date]:
    """
    Given a reference (year, month) and closing_day, return purchase date range
    (start, end) inclusive for that invoice: (prev_closing+1, current_closing).
    """
    curr_close = _closing_date(year, month, closing_day)
    prev_year, prev_month = _add_month(year, month, -1)
    prev_close = _closing_date(prev_year, prev_month, closing_day)
    start = prev_close + timedelta(days=1)
    end = curr_close
    return start, end


def _due_date_for_reference(year: int, month: int, closing_day: int, due_day: int) -> date:
    # Typically due is in same or next month; choose next month if due <= closing
    from calendar import monthrange

    due_year, due_month = (year, month)
    if due_day <= closing_day:
        due_year, due_month = _add_month(year, month, 1)
    last = monthrange(due_year, due_month)[1]
    day = min(max(1, due_day), last)
    return date(due_year, due_month, day)


@transaction.atomic
def build_invoice_for(card: CreditCard, year: int, month: int) -> CardInvoice:
    start, end = _cycle_range(year, month, card.closing_day)
    from django.db.models import Sum
    total = (
        CardTransaction.objects.filter(card=card, purchase_date__gte=start, purchase_date__lte=end)
        .aggregate(total=Sum('amount'))['total']
        or 0
    )
    reference = f"{year:04d}-{month:02d}"
    closing_date = _closing_date(year, month, card.closing_day)
    due_date = _due_date_for_reference(year, month, card.closing_day, card.due_day)
    inv, _ = CardInvoice.objects.update_or_create(
        card=card,
        reference_yyyy_mm=reference,
        defaults={
            'closing_date': closing_date,
            'due_date': due_date,
            'total_calculated': total,
            'status': CardInvoice.STATUS_OPEN,
        },
    )
    return inv


def _sum_amount(qs) -> float:
    from django.db.models import Sum

    return qs.aggregate(total=Sum('amount'))['total'] or 0


@transaction.atomic
def rebuild_invoices_for_card(card: CreditCard) -> List[CardInvoice]:
    # Determine all (year, month) from transactions for this card
    qs = CardTransaction.objects.filter(card=card)
    refs = set((t.purchase_date.year, t.purchase_date.month) for t in qs.only('purchase_date'))
    out: List[CardInvoice] = []
    for y, m in sorted(refs):
        out.append(build_invoice_for(card, y, m))
    return out


@transaction.atomic
def rebuild_invoices_for_user(user, card_id: Optional[int] = None) -> int:
    cards = CreditCard.objects.filter(user=user)
    if card_id:
        cards = cards.filter(id=card_id)
    count = 0
    for c in cards:
        invs = rebuild_invoices_for_card(c)
        count += len(invs)
    return count
