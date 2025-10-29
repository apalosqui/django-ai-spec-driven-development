from datetime import datetime

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import compute_projection

from .models import SalaryRule, FixedExpense, VariableBudget
from .serializers import SalaryRuleSerializer, FixedExpenseSerializer, VariableBudgetSerializer


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
