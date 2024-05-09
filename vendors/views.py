from .models import Vendor
from django.db import models
from .serializers import VendorSerializer
from .models import Vendor
from purchase_orders.models import PurchaseOrders

from rest_framework import generics, viewsets
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

    def calculate_quality_rating_average(vendor_id):
        completed_purchase_order = PurchaseOrders.objects.filter(
            vendor_id=vendor_id, delivery_date__isnull=False
        )
        quality_rating_avg = completed_purchase_order.aggregate(
            Avg('quality_rating_avg')
        )['quality_rating_avg__avg']
        return quality_rating_avg        

class QualityRatingAvgViewSet(viewsets.ViewSet):
    def update_quality_rating_avg(self, request):
        # Retrieving the vendor assuming its id is provided in request
        vendor_id = request.data.get('vendor_id')
        vendor = Vendor.objects.get(id=vendor_id)

        completed_purchase_orders = PurchaseOrders.objects.filter(
            vendor=vendor,
            status='COMPLETE',
            quality_rating__isnull=False
        )

        total_ratings = completed_purchase_orders.count()
        total_ratings_sum = completed_purchase_orders.aggregate(
            models.Sum('quality_rating')
        )['quality_rating__sum']
        if total_ratings > 0: average_rating = total_ratings_sum / total_ratings
        else: average_rating = None

        # Update quality_rating_avg field of the vendor
        vendor.quality_rating_avg = average_rating
        vendor.save()

        return Response({
            'message': 'Quality rating average updated succesfully'
        })
