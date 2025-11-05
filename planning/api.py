from datetime import datetime

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import compute_projection

from .models import SalaryRule, FixedExpense, VariableBudget
from .serializers import SalaryRuleSerializer, FixedExpenseSerializer, VariableBudgetSerializer
from django.http import HttpResponse
from datetime import date
import calendar
import csv
from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction
from .models import FixedExpense, SalaryRule, VariableBudget
from django.utils.dateparse import parse_date


class BaseOwnedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SalaryRuleViewSet(BaseOwnedViewSet):
    serializer_class = SalaryRuleSerializer

    def get_queryset(self):
        return SalaryRule.objects.filter(user=self.request.user)


class FixedExpenseViewSet(BaseOwnedViewSet):
    serializer_class = FixedExpenseSerializer

    def get_queryset(self):
        return FixedExpense.objects.filter(user=self.request.user)


class VariableBudgetViewSet(BaseOwnedViewSet):
    serializer_class = VariableBudgetSerializer

    def get_queryset(self):
        return VariableBudget.objects.filter(user=self.request.user)


class ProjectionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_str = request.query_params.get('start')
        months = int(request.query_params.get('months', 24))
        if not start_str:
            return Response({'detail': 'start is required (YYYY-MM-DD)'}, status=400)
        try:
            start = datetime.strptime(start_str, '%Y-%m-%d').date()
        except Exception:
            return Response({'detail': 'invalid start (YYYY-MM-DD)'}, status=400)
        data = compute_projection(request.user, start, months)
        return Response(data)


class ExportCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Accept either (year, month) or explicit (start, end)
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        start_str = request.query_params.get('start')
        end_str = request.query_params.get('end')

        if year and month:
            try:
                y = int(year)
                m = int(month)
                first_day = date(y, m, 1)
                last_day = date(y, m, calendar.monthrange(y, m)[1])
            except Exception:
                return Response({'detail': 'invalid year/month'}, status=400)
        elif start_str and end_str:
            try:
                first_day = datetime.strptime(start_str, '%Y-%m-%d').date()
                last_day = datetime.strptime(end_str, '%Y-%m-%d').date()
                if last_day < first_day:
                    raise ValueError('end before start')
            except Exception:
                return Response({'detail': 'invalid start/end (YYYY-MM-DD)'}, status=400)
        else:
            return Response({'detail': 'provide year+month or start+end'}, status=400)

        # Compute projection from the beginning of the selected year up to the selected month
        base_start = date(first_day.year, 1, 1)
        months_span = (last_day.year - base_start.year) * 12 + last_day.month
        series = compute_projection(request.user, base_start, months_span)

        start_iso = first_day.isoformat()
        end_iso = last_day.isoformat()
        rows = [d for d in series if start_iso <= d['date'] <= end_iso]

        # Build CSV
        resp = HttpResponse(content_type='text/csv; charset=utf-8')
        filename = f'relatorio_{first_day.strftime("%Y-%m")}.csv'
        resp['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(resp)
        writer.writerow(['Data', 'Entrada', 'Saida', 'Diario', 'Saldo'])
        for d in rows:
            # Dates in DD-MM-YYYY; values as floats (non-negative for entrada/saida/diario)
            data_br = '-'.join(d['date'].split('-')[::-1])
            writer.writerow([
                data_br,
                f"{float(d.get('entrada') or 0):.2f}",
                f"{float(d.get('saida') or 0):.2f}",
                f"{float(d.get('diario') or 0):.2f}",
                f"{float(d.get('saldo') or 0):.2f}",
            ])

        return resp


class QuickEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        kind = (request.data.get('kind') or '').strip()  # income|expense|monthly_average
        amount = request.data.get('amount')
        date_str = request.data.get('date')
        desc = (request.data.get('description') or '').strip()
        recurrence = (request.data.get('recurrence') or 'once').strip()  # once|monthly
        expense_mode = (request.data.get('expense_mode') or 'fixed').strip()  # fixed|daily (aplica para expense)
        backfill = str(request.data.get('backfill') or 'false').lower() in ('1','true','yes','on')
        backfill_since = request.data.get('backfill_since')

        if kind not in ('income', 'expense', 'monthly_average'):
            return Response({'detail': 'kind must be income, expense, or monthly_average'}, status=400)
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except Exception:
            return Response({'detail': 'amount must be positive'}, status=400)

        # Unified account + default category
        acc, _ = Account.objects.get_or_create(user=request.user, name='Conta Única', defaults={'opening_balance': 0, 'kind': getattr(Account, 'KIND_CASH', 'CAIXA')})

        # Monthly Average (Variable Budget - diluído durante o mês)
        if kind == 'monthly_average':
            vb, created = VariableBudget.objects.update_or_create(
                user=request.user,
                category='Gastos Variáveis',
                defaults={'monthly_amount': amount, 'active': True}
            )
            # Apply backfill if requested
            if backfill and backfill_since:
                bf_date = parse_date(backfill_since)
                if bf_date:
                    VariableBudget.objects.filter(pk=vb.pk).update(created_at=bf_date)
            return Response({
                'status': 'ok',
                'created': 'variable_budget',
                'monthly_amount': amount,
                'note': 'Este valor será diluído diariamente ao longo do mês'
            }, status=201)

        # Parse date for income/expense (not needed for monthly_average)
        d = parse_date(date_str)
        if not d:
            return Response({'detail': 'invalid date (YYYY-MM-DD)'}, status=400)

        # Determine backfill date
        bf_date = parse_date(backfill_since) if (backfill and backfill_since) else None

        cat, _ = Category.objects.get_or_create(user=request.user, name='Outros', type=kind if kind != 'monthly_average' else 'expense')

        # Income
        if kind == 'income':
            if recurrence == 'monthly':
                # Create/update salary rule on the same day of month
                rule, _ = SalaryRule.objects.update_or_create(
                    user=request.user,
                    defaults={'amount': amount, 'days': str(d.day), 'ultimo_dia_util': False},
                )
                if bf_date:
                    # move created_at to bf_date to aplicar retroativamente
                    SalaryRule.objects.filter(pk=rule.pk).update(created_at=bf_date)
                return Response({'status': 'ok', 'created': 'salary_rule', 'amount': amount, 'day': d.day, 'backfill': backfill}, status=201)
            else:
                tx = Transaction.objects.create(account=acc, category=cat, amount=amount, kind='income', date=d, description=desc)
                return Response({'id': tx.id, 'kind': 'income', 'amount': amount, 'date': d.isoformat()}, status=201)

        # Expense
        if expense_mode == 'daily':
            # Daily expense: create Transaction for specific day only (vai para coluna "Diário")
            # Usa marcador [DIARIO] na descrição para identificar no compute_projection
            tx = Transaction.objects.create(
                account=acc,
                category=cat,
                amount=amount,
                kind='expense',
                date=d,
                description=f'[DIARIO] {desc}' if desc else '[DIARIO] Despesa diária'
            )
            return Response({
                'id': tx.id,
                'kind': 'expense',
                'amount': amount,
                'date': d.isoformat(),
                'note': 'Despesa registrada na coluna Diário (substitui valor variável)'
            }, status=201)
        else:
            # expense_mode == 'fixed'
            if recurrence == 'monthly':
                # Despesa fixa recorrente mensal -> FixedExpense (vai para "Saída")
                fx = FixedExpense.objects.create(
                    user=request.user,
                    name=desc or 'Despesa Fixa',
                    amount=amount,
                    due_day=d.day,
                    periodicity='MENSAL',
                    pay_early_business_day=False,
                    paying_account=acc
                )
                if bf_date:
                    FixedExpense.objects.filter(pk=fx.pk).update(created_at=bf_date)
                return Response({'status': 'ok', 'created': 'fixed_expense', 'amount': amount, 'day': d.day, 'backfill': backfill}, status=201)
            else:
                # Despesa fixa pontual (única) -> Transaction SEM marcador (vai para "Saída")
                tx = Transaction.objects.create(
                    account=acc,
                    category=cat,
                    amount=amount,
                    kind='expense',
                    date=d,
                    description=desc or 'Despesa única'
                )
                return Response({
                    'id': tx.id,
                    'kind': 'expense',
                    'amount': amount,
                    'date': d.isoformat(),
                    'note': 'Despesa registrada na coluna Saída'
                }, status=201)
