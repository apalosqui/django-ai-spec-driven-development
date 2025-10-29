from __future__ import annotations

from datetime import date

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from planning.services import compute_projection


class Command(BaseCommand):
    help = 'Print month-end balances to validate carry-over. Default user: carry@demo.com.'

    def add_arguments(self, parser):
        parser.add_argument('--email', default='carry@demo.com')
        parser.add_argument('--start', default='2025-01-01')
        parser.add_argument('--months', default=12, type=int)

    def handle(self, *args, **opts):
        email = opts['email']
        start = date.fromisoformat(opts['start'])
        months = int(opts['months'])
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stderr.write('User not found. Run seed_carry_demo first.')
            return

        data = compute_projection(user, start, months=months)
        # Collect last day per month
        by_month = {}
        for row in data:
            y, m, _ = row['date'].split('-')
            key = f'{y}-{m}'
            by_month[key] = row  # last assignment wins (last day)
        keys = sorted(by_month.keys())
        prev = None
        self.stdout.write('Month\tSaldo\tDelta')
        for k in keys:
            saldo = float(by_month[k]['saldo'])
            delta = saldo - prev if prev is not None else 0.0
            self.stdout.write(f'{k}\t{saldo:.2f}\t{delta:.2f}')
            prev = saldo

