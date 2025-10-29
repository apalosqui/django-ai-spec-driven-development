from django.conf import settings
from django.db import models


class SalaryRule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='salary_rules')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    days = models.CharField(max_length=50, blank=True, help_text='Comma-separated days, e.g., 5,20')
    ultimo_dia_util = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'SalaryRule({self.user_id}, {self.amount})'


class FixedExpense(models.Model):
    PERIODICITY_MONTHLY = 'MENSAL'
    PERIODICITY_ANNUAL = 'ANUAL'
    PERIODICITY_CHOICES = (
        (PERIODICITY_MONTHLY, 'Mensal'),
        (PERIODICITY_ANNUAL, 'Anual'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fixed_expenses')
    name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_day = models.PositiveSmallIntegerField()
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES, default=PERIODICITY_MONTHLY)
    pay_early_business_day = models.BooleanField(default=False)
    paying_account = models.ForeignKey('accounts.Account', on_delete=models.PROTECT, related_name='fixed_expenses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.amount})'


class VariableBudget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='variable_budgets')
    category = models.CharField(max_length=150)
    monthly_amount = models.DecimalField(max_digits=12, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.category}: {self.monthly_amount}'

