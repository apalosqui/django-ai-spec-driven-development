from django.contrib import admin

from .models import SalaryRule, FixedExpense, VariableBudget


@admin.register(SalaryRule)
class SalaryRuleAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'days', 'ultimo_dia_util', 'created_at')
    search_fields = ('user__email', 'days')


@admin.register(FixedExpense)
class FixedExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'amount', 'due_day', 'periodicity', 'paying_account')
    search_fields = ('user__email', 'name')


@admin.register(VariableBudget)
class VariableBudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'monthly_amount', 'active')
    search_fields = ('user__email', 'category')

