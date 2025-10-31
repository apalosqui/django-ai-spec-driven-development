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
