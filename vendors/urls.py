from django.urls import path, include
from . import views
from .views import VendorViewSet
from rest_framework import views as rest_views
from rest_framework.routers import DefaultRouter
from purchase_orders.views import PurchaseOrderViewSet

# router = DefaultRouter()
# router.register('purchase-orders', Purchase)

urlpatterns = [
    #path('', rest_views.as_view(), ),
    path('', views.VendorsList.as_view(), name='vendorlist'),
    path('<int:pk>/', views.VendorsDetail.as_view(), name='vendordetail'),
    path('<int:pk>/quality_rating_average/', VendorViewSet.as_view({'get': 'quality_rating_average'}), name='quality_rating_average'),
    # path('<int:pk>/complete/', VendorViewSet.calculate_quality_rating_average, name='complete_purchase_order'),
]

