from __future__ import annotations

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import Account
from planning.models import SalaryRule, FixedExpense, VariableBudget


class Command(BaseCommand):
    help = 'Seed deterministic carry-over demo data starting 2025-01-15.'

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            email='carry@demo.com', defaults={'is_active': True}
        )
        if created or not user.has_usable_password():
            user.set_password('demo12345')
            user.save(update_fields=['password'])

        cash, _ = Account.objects.get_or_create(
            user=user,
            name='Carteira',
            defaults={'opening_balance': 0, 'kind': Account.KIND_CASH},
        )
        Account.objects.get_or_create(
            user=user,
            name='Reserva',
            defaults={'opening_balance': 0, 'kind': Account.KIND_SAVINGS},
        )

        SalaryRule.objects.update_or_create(
            user=user,
            days='15',
            defaults={'amount': 2000, 'ultimo_dia_util': False},
        )

        FixedExpense.objects.update_or_create(
            user=user,
            name='Contas Fixas',
            defaults={'amount': 500, 'due_day': 25, 'periodicity': FixedExpense.PERIODICITY_MONTHLY, 'pay_early_business_day': False, 'paying_account': cash},
        )

        VariableBudget.objects.update_or_create(
            user=user, category='Variáveis', defaults={'monthly_amount': 500, 'active': True}
        )

        self.stdout.write(self.style.SUCCESS('Seed carry-over demo ready.'))
        self.stdout.write('Login: carry@demo.com  Senha: demo12345')

