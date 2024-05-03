from django.shortcuts import render
from .models import PurchaseOrders
from .serializers import PurchaseOrderSerializer
from rest_framework import generics

# Create your views here.

class PurchaseOrdersList(generics.ListCreateAPIView):
    queryset = PurchaseOrders.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrders.objects.all()
    serializer_class = PurchaseOrderSerializer
