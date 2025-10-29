from rest_framework import serializers

from .models import SalaryRule, FixedExpense, VariableBudget


class SalaryRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryRule
        fields = ['id', 'amount', 'days', 'ultimo_dia_util', 'created_at', 'updated_at']


class FixedExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedExpense
        fields = ['id', 'name', 'amount', 'due_day', 'periodicity', 'pay_early_business_day', 'paying_account', 'created_at', 'updated_at']


class VariableBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariableBudget
        fields = ['id', 'category', 'monthly_amount', 'active', 'created_at', 'updated_at']

