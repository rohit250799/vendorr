from django.urls import path, include
from . import views
from vendors.views import VendorViewSet
from rest_framework import views as po_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('purchase-orders', views.PurchaseOrderViewSet,
                 basename='purchase-order')
router.register('vendors', VendorViewSet, basename='vendorvs')


urlpatterns = [
    path('', views.PurchaseOrdersList.as_view(), name='purchaseorderlist'),
    path('<int:pk>/', views.PurchaseOrderDetail.as_view(), name='purchaseorderdetail'),
    path('router/', include(router.urls)),
    path('on_time_delivery_rate/<int:vendor_id>/', 
         views.PurchaseOrderViewSet.as_view({'get': 'on_time_delivery_rate'}), 
         name='on_time_delivery_rate'),
    path('<int:pk>/mark_completed/', views.PurchaseOrderViewSet.as_view({
        'post': 'mark_completed'
    }), name='complete-purchase-order'),
    
]
