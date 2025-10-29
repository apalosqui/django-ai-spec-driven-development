from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'opening_balance', 'archived', 'kind', 'tag_color', 'created_at', 'updated_at']

