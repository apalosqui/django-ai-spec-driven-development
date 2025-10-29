from django.conf import settings
from django.db import models


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=150)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    archived = models.BooleanField(default=False)
    KIND_CASH = 'CAIXA'
    KIND_SAVINGS = 'ECONOMIA'
    KIND_CHOICES = (
        (KIND_CASH, 'Caixa'),
        (KIND_SAVINGS, 'Economia'),
    )
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default=KIND_CASH)
    tag_color = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
