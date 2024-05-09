from django.db.models import F
from .models import PurchaseOrders
from .signals import update_quality_rating_average
from .serializers import PurchaseOrderSerializer
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

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
            vendor_id=vendor_id, status='COMPLETE')

        on_time_count = completed_purchase_order.filter(
            delivery_date__lte=F('delivery_date')).count()
        
        total_count = completed_purchase_order.count()
        if total_count == 0: return Response(
            {'on_time_delivery_rate': 0}
        )

        on_time_delivery_rate = (on_time_count / total_count) * 100
        return Response({
            'on_time_delivery_rate': on_time_delivery_rate,
        })
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        #pk = purchase_order.id
        purchase_order = self.get_object()
        purchase_order.status = 'COMPLETE'
        purchase_order.save()
        return Response({
            'message': 'Purchase order is completed'
        }, status=status.HTTP_200_OK)

