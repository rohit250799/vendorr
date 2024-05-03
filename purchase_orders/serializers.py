from rest_framework import serializers
from .models import PurchaseOrders

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrders
        fields = '__all__'
        