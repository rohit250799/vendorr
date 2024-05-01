from django.shortcuts import render

from .models import Vendor
from .serializers import VendorSerializer

from rest_framework import generics

# Create your views here.

class VendorsList(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer