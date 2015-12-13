from rest_framework import serializers
from main.models import Receipt

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ('user', 'date', 'description', 'store')