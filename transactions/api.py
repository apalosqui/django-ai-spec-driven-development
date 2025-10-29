from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Transfer, TransactionLog, ProjectionSnapshot
from .serializers import TransferSerializer, TransactionLogSerializer, ProjectionSnapshotSerializer


class BaseOwnedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]


class TransferViewSet(BaseOwnedViewSet):
    serializer_class = TransferSerializer

    def get_queryset(self):
        return Transfer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionLogViewSet(BaseOwnedViewSet):
    serializer_class = TransactionLogSerializer

    def get_queryset(self):
        return TransactionLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProjectionSnapshotViewSet(BaseOwnedViewSet):
    serializer_class = ProjectionSnapshotSerializer

    def get_queryset(self):
        return ProjectionSnapshot.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

