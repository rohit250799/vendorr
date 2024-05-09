from django.urls import path
from . import views
from .views import VendorViewSet


urlpatterns = [
    path('', views.VendorsList.as_view(), name='vendorlist'),
    path('<int:pk>/', views.VendorsDetail.as_view(), name='vendordetail'),
    path('<int:pk>/quality_rating_average/', VendorViewSet.as_view({'get': 'quality_rating_average'}), name='quality_rating_average_get'),
    path('update_quality_rating_avg/', views.QualityRatingAvgViewSet.as_view({'post': 'update_quality_rating_avg'}), name='quality-rating-avg_update'),
]

