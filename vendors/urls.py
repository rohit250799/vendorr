from django.urls import path
from . import views
from rest_framework import views as rest_views

    
urlpatterns = [
    #path('', rest_views.as_view(), ),
    path('', views.VendorsList.as_view(), name='vendorlist'),
    path('<int:pk>/', views.VendorsDetail.as_view(), name='vendordetail'),
]

