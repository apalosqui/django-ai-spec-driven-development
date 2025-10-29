from django.db import models

from accounts.models import Account
from categories.models import Category


class Transfer(models.Model):
    TYPE_APPLY = 'APLICACAO'
    TYPE_REDEEM = 'RESGATE'
    TYPE_CHOICES = (
        (TYPE_APPLY, 'Aplicação'),
        (TYPE_REDEEM, 'Resgate'),
    )

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='transfers')
    origin = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transfers_out')
    destination = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='transfers_in')
    value = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    kind = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.kind} {self.value} {self.date}'


class TransactionLog(models.Model):
    TYPE_SALARY = 'SALARIO'
    TYPE_FIXED = 'FIXO'
    TYPE_VARIABLE = 'VARIAVEL'
    TYPE_INVOICE = 'FATURA'
    TYPE_TRANSFER = 'TRANSFER'
    TYPE_CHOICES = (
        (TYPE_SALARY, 'Salário'),
        (TYPE_FIXED, 'Fixo'),
        (TYPE_VARIABLE, 'Variável'),
        (TYPE_INVOICE, 'Fatura'),
        (TYPE_TRANSFER, 'Transferência'),
    )

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='transaction_logs')
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    ref_id = models.CharField(max_length=50, blank=True)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.type} {self.value} {self.date}'


class ProjectionSnapshot(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='projection_snapshots')
    date = models.DateField()
    projected_balance = models.DecimalField(max_digits=12, decimal_places=2)
    meta_info_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f'{self.user_id} {self.date} {self.projected_balance}'


class Transaction(models.Model):
    KIND_CHOICES = (
        ('income', 'Receita'),
        ('expense', 'Despesa'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    kind = models.CharField(max_length=7, choices=KIND_CHOICES)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return f'{self.get_kind_display()} {self.amount} · {self.date}'
