from __future__ import annotations

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import Account
from planning.models import SalaryRule, FixedExpense, VariableBudget
from cards.models import CreditCard, CardTransaction
from cards.services import rebuild_invoices_for_user
from transactions.models import Transfer


class Command(BaseCommand):
    help = 'Seed demo data for user 123@gmail.com to test projection.'

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            email='123@gmail.com', defaults={'is_active': True}
        )
        if created or not user.has_usable_password():
            user.set_password('12345678')
            user.save(update_fields=['password'])

        # Accounts
        cash, _ = Account.objects.get_or_create(
            user=user,
            name='Carteira',
            defaults={'opening_balance': 1000, 'kind': Account.KIND_CASH, 'tag_color': '#3b82f6'},
        )
        savings, _ = Account.objects.get_or_create(
            user=user,
            name='Reserva',
            defaults={'opening_balance': 5000, 'kind': Account.KIND_SAVINGS, 'tag_color': '#22c55e'},
        )

        # Salary rule (day 5)
        SalaryRule.objects.update_or_create(
            user=user, days='5', defaults={'amount': 4000, 'ultimo_dia_util': False}
        )

        # Fixed expenses
        FixedExpense.objects.update_or_create(
            user=user, name='Aluguel', defaults={'amount': 1500, 'due_day': 10, 'periodicity': FixedExpense.PERIODICITY_MONTHLY, 'pay_early_business_day': False, 'paying_account': cash}
        )
        FixedExpense.objects.update_or_create(
            user=user, name='Internet', defaults={'amount': 120, 'due_day': 15, 'periodicity': FixedExpense.PERIODICITY_MONTHLY, 'pay_early_business_day': False, 'paying_account': cash}
        )

        # Variable budgets
        VariableBudget.objects.update_or_create(user=user, category='Mercado', defaults={'monthly_amount': 900, 'active': True})
        VariableBudget.objects.update_or_create(user=user, category='Lazer', defaults={'monthly_amount': 300, 'active': True})

        # Credit card
        card, _ = CreditCard.objects.get_or_create(
            user=user,
            name='Visa',
            defaults={'closing_day': 5, 'due_day': 15, 'paying_account': cash},
        )

        # Card transactions (some in current and previous cycles)
        today = date.today()
        purchases = [
            (today - timedelta(days=12), 'Restaurante', 'Alimentação', 85.50),
            (today - timedelta(days=25), 'Mercado XYZ', 'Mercado', 240.75),
            (today - timedelta(days=3), 'Transporte', 'Transporte', 42.30),
        ]
        for d, desc, cat, amt in purchases:
            CardTransaction.objects.get_or_create(
                card=card,
                purchase_date=d,
                description=desc,
                category=cat,
                amount=amt,
            )

        # Transfers (application and redeem)
        Transfer.objects.get_or_create(
            user=user,
            origin=cash,
            destination=savings,
            value=500,
            date=today - timedelta(days=7),
            kind=Transfer.TYPE_APPLY,
        )
        Transfer.objects.get_or_create(
            user=user,
            origin=savings,
            destination=cash,
            value=200,
            date=today - timedelta(days=2),
            kind=Transfer.TYPE_REDEEM,
        )

        # Build invoices
        rebuilt = rebuild_invoices_for_user(user)

        self.stdout.write(self.style.SUCCESS('Seed completed.'))
        self.stdout.write('Login email: 123@gmail.com  password: 12345678')
        self.stdout.write(f'Invoices rebuilt: {rebuilt}')

