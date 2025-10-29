from django.conf import settings
from django.db import models


class CreditCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_cards')
    name = models.CharField(max_length=100)
    closing_day = models.PositiveSmallIntegerField(help_text='Dia de fechamento (1-31)')
    due_day = models.PositiveSmallIntegerField(help_text='Dia de vencimento (1-31)')
    paying_account = models.ForeignKey('accounts.Account', on_delete=models.PROTECT, related_name='credit_cards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.user_id})'


class CardTransaction(models.Model):
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name='transactions')
    purchase_date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=120, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    installments = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.card_id} {self.amount} {self.purchase_date}'


class CardInvoice(models.Model):
    STATUS_OPEN = 'ABERTA'
    STATUS_PAID = 'PAGA'
    STATUS_CHOICES = (
        (STATUS_OPEN, 'Aberta'),
        (STATUS_PAID, 'Paga'),
    )

    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name='invoices')
    reference_yyyy_mm = models.CharField(max_length=7)
    closing_date = models.DateField()
    due_date = models.DateField()
    total_calculated = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('card', 'reference_yyyy_mm')

    def __str__(self):
        return f'Invoice {self.card_id} {self.reference_yyyy_mm}'

