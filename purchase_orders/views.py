from django.shortcuts import render
from django.db.models import F
from .models import PurchaseOrders
from .serializers import PurchaseOrderSerializer
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.

class PurchaseOrdersList(generics.ListCreateAPIView):
    queryset = PurchaseOrders.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrders.objects.all()
    serializer_class = PurchaseOrderSerializer


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrders.objects.all()
    serializer_class = PurchaseOrderSerializer

    @action(detail=False, methods=['get'])
    def on_time_delivery_rate(self, request, vendor_id=None):
        if not vendor_id: return Response(
            {'error': 'Vendor id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
        completed_purchase_order = PurchaseOrders.objects.filter(
            vendor_id=vendor_id, status='completed')
        on_time_count = completed_purchase_order.filter(
            delivery_date__lte=F('delivery_date')).count()
        total_count = completed_purchase_order.count()
        if total_count == 0: return Response(
            {'on_time_delivery_rate': 0}
        )
        on_time_delivery_rate = (on_time_count / total_count) * 100
        return Response({
            'on_time_delivery_rate': on_time_delivery_rate
        })