from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import CreditCard, CardTransaction, CardInvoice
from .serializers import CreditCardSerializer, CardTransactionSerializer, CardInvoiceSerializer
from .services import build_invoice_for, rebuild_invoices_for_user


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

    @action(detail=False, methods=['get'])
    def compute(self, request):
        """
        Compute (or refresh) an invoice for the given card and yyyy_mm.
        Params: card_id (int), yyyy_mm (YYYY-MM)
        """
        card_id = request.query_params.get('card_id')
        yyyy_mm = request.query_params.get('yyyy_mm')
        if not card_id or not yyyy_mm:
            return Response({'detail': 'card_id and yyyy_mm are required'}, status=400)
        try:
            year, month = map(int, yyyy_mm.split('-'))
        except Exception:
            return Response({'detail': 'invalid yyyy_mm'}, status=400)
        try:
            card = CreditCard.objects.get(id=card_id, user=request.user)
        except CreditCard.DoesNotExist:
            return Response({'detail': 'card not found'}, status=404)
        inv = build_invoice_for(card, year, month)
        return Response(self.get_serializer(inv).data)

    @action(detail=False, methods=['post'])
    def rebuild(self, request):
        """
        Rebuild invoices for current user; optionally filter by card_id.
        Body: { "card_id": optional int }
        """
        card_id = request.data.get('card_id')
        try:
            card_id = int(card_id) if card_id is not None else None
        except Exception:
            return Response({'detail': 'invalid card_id'}, status=400)
        count = rebuild_invoices_for_user(request.user, card_id=card_id)
        return Response({'rebuilt': count})
