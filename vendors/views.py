from .models import Vendor
from django.db import models
from .serializers import VendorSerializer
from .models import Vendor
from purchase_orders.models import PurchaseOrders

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Avg, F, ExpressionWrapper, DurationField, Func, IntegerField

# Create your views here.

class VendorsList(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class ExtractEpoch(Func):
    function = 'Extract'
    template = '%(function)s(EPOCH FROM %(expressions)s)'
    output_field = IntegerField()

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

    @action(detail=True, methods=['get'])
    def average_response_time(self, request, pk=None):
        average_time = PurchaseOrders.objects.exclude(
            acknowledgement_date__isnull=True).aggregate(avg_time=Avg(
                models.ExpressionWrapper(models.F('acknowledgement_date') - models.F(
                    'issue_date'), output_field=models.DurationField())))['avg_time']
        return Response({
            'average_response_time': average_time.total_seconds() if average_time else None
        }, status=status.HTTP_200_OK)    

    def calculate_average_response_time(vendor_id):
        acknowledged_purchase_order = PurchaseOrders.objects.filter(
            vendor_id=vendor_id, issue_date__isnull = False
        )    
        average_response_time = acknowledged_purchase_order.aggregate(Avg('average_response_time'))['average_response_time__avg']
        average_response_time_days = average_response_time.total_seconds() / (60*60*24) if average_response_time else None
        return average_response_time_days

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

class AverageResponseTimeViewSet(viewsets.ViewSet):
    def update_average_response_time(self, request):
        vendor_id = request.data.get('vendor_id')
        vendor = Vendor.objects.get(id=vendor_id)

        acknowledged_purchase_orders = PurchaseOrders.objects.filter(
            vendor=vendor,
            issue_date__isnull = False,
            acknowledgement_date__isnull = False
        )

        acknowledged_purchase_orders = acknowledged_purchase_orders.annotate(
            response_time_seconds = ExpressionWrapper(ExtractEpoch(F('acknowledgement_date') - F('issue_date')), output_field=IntegerField())
        )
        
        average_response_time = acknowledged_purchase_orders.aggregate(avg_response_time = Avg('response_time_seconds'))['avg_response_time']

        def convert_seconds_to_hours(seconds):
            if seconds is None or seconds < 0: return None
            seconds = int(seconds)
            hours, seconds = divmod(seconds, 3600)
            return hours

        average_response_time_days = average_response_time / (60*60) if average_response_time else None

        vendor.average_response_time = average_response_time_days
        vendor.save()

        return Response({
            'message': 'Average response time updated succesfully'
        })