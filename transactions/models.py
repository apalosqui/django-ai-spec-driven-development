from django.db import models

from accounts.models import Account
from categories.models import Category


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
