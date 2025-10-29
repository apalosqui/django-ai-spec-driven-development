from rest_framework import serializers

from .models import Transfer, TransactionLog, ProjectionSnapshot


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['id', 'origin', 'destination', 'value', 'date', 'kind', 'created_at', 'updated_at']


class TransactionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLog
        fields = ['id', 'date', 'type', 'ref_id', 'value', 'created_at', 'updated_at']


class ProjectionSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectionSnapshot
        fields = ['id', 'date', 'projected_balance', 'meta_info_json', 'created_at', 'updated_at']

