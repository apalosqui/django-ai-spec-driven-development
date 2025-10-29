from rest_framework import serializers

from .models import CreditCard, CardTransaction, CardInvoice


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['id', 'name', 'closing_day', 'due_day', 'paying_account', 'created_at', 'updated_at']


class CardTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardTransaction
        fields = ['id', 'card', 'purchase_date', 'description', 'category', 'amount', 'installments', 'created_at', 'updated_at']


class CardInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardInvoice
        fields = ['id', 'card', 'reference_yyyy_mm', 'closing_date', 'due_date', 'total_calculated', 'status', 'created_at', 'updated_at']

