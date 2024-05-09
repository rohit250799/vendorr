from .models import Vendor
from .serializers import VendorSerializer
from .models import Vendor
from purchase_orders.models import PurchaseOrders

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Avg

# Create your views here.

class VendorsList(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=['get'])
    def quality_rating_average(self, request, pk=None):
        vendor = self.get_object()
        #quality_rating_average = vendor.quality_rating_avg()
        quality_rating_average = vendor.quality_rating_avg
        return Response({
            'quality_rating_average': quality_rating_average
        })
    
    # @action(detail=True, methods=['post'])
    # def complete(self, request, vendor_id=None):
    #     purchase_order = self.get_object()
    #     quality_rating = request.data.get('quality_rating')

    #     if quality_rating is not None:
    #         purchase_order.quality_rating = quality_rating
    #         purchase_order.status = 'COMPLETE'
    #         purchase_order.save()

    #         vendor = purchase_order.vendor
    #         vendor.quality_rating_avg = Vendor.update_quality_rating_average()

    #         return Response({
    #             'status': 'Purchase order completed succesfully.'
    #         })
    #     else: return Response({
    #         'error': 'Quality rating is required'
    #     }, status=status.HTTP_400_BAD_REQUEST)

    def calculate_quality_rating_average(vendor_id):
        completed_purchase_order = PurchaseOrders.objects.filter(
            vendor_id=vendor_id, delivery_date__isnull=False
        )
        quality_rating_avg = completed_purchase_order.aggregate(
            Avg('quality_rating_avg')
        )['quality_rating_avg__avg']
        return quality_rating_avg        
