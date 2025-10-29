from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import CreditCard, CardTransaction, CardInvoice
from .serializers import CreditCardSerializer, CardTransactionSerializer, CardInvoiceSerializer


class BaseOwnedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]


class CreditCardViewSet(BaseOwnedViewSet):
    serializer_class = CreditCardSerializer

    def get_queryset(self):
        return CreditCard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CardTransactionViewSet(BaseOwnedViewSet):
    serializer_class = CardTransactionSerializer

    def get_queryset(self):
        return CardTransaction.objects.filter(card__user=self.request.user)


class CardInvoiceViewSet(BaseOwnedViewSet):
    serializer_class = CardInvoiceSerializer

    def get_queryset(self):
        return CardInvoice.objects.filter(card__user=self.request.user)

