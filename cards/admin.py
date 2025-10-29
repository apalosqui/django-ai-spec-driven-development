from django.contrib import admin

from .models import CreditCard, CardTransaction, CardInvoice


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'closing_day', 'due_day', 'paying_account')
    search_fields = ('user__email', 'name')


@admin.register(CardTransaction)
class CardTransactionAdmin(admin.ModelAdmin):
    list_display = ('card', 'purchase_date', 'amount', 'category')
    search_fields = ('description', 'category')


@admin.register(CardInvoice)
class CardInvoiceAdmin(admin.ModelAdmin):
    list_display = ('card', 'reference_yyyy_mm', 'due_date', 'total_calculated', 'status')
    search_fields = ('reference_yyyy_mm',)

