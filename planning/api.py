from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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

