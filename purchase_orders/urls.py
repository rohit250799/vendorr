from django.urls import path
from . import views
from rest_framework import views as po_views

urlpatterns = [
    path('', views.PurchaseOrdersList.as_view(), name='purchaseorderlist'),
    path('<int:pk>/', views.PurchaseOrderDetail.as_view(), name='purchaseorderdetail'),
]
