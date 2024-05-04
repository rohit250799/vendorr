from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import PurchaseOrders
from vendors.models import Vendor

from rest_framework import status
from rest_framework.test import APIClient

# Order is placed by the buyer before the purchase order is issued to the vendor(order date < issue date)
class PurchaseOrdersViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name="Shivam Test Vendor",
            # contact_details = "Testing contact details",
            # address = "2 Central Street, Kolkata",
            # vendor_code = 23,
            on_time_delivery_rate = 57.33,
            quality_rating_avg = 34.4,
            average_response_time = 58,
            fulfillment_rate = 49.9,
        )

    def test_on_time_delivery_rate_no_completed_orders(self):
        #Testing on time delivery rate custom action with 0 completed purchase orders
        url = reverse('on_time_delivery_rate', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['on_time_delivery_rate'], 0)

    def test_on_time_delivery_rate_with_completed_orders(self):
        #Testing on time delivery rate custom action with completed purchase orders
        on_time_purchase_order = PurchaseOrders.objects.create(
            po_number = 2241,
            vendor = 2,
            delivery_date = timezone.now() + timezone.timedelta(days=5),
            status = "COMPLETED",
        )

        late_purchase_order = PurchaseOrders.objects.create(
            po_number = 294,
            vendor = 2,
            delivery_date = timezone.now() + timezone.timedelta(days=5),
            status = "COMPLETED",
        )

        url = reverse('on_time_delivery_rate', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['on_time_delivery_rate'], 50.0)

    def test_on_time_delivery_rate_invalid_vendor_id(self):
        #Test the on_time_delivery_rate custom action with an invalid vendor ID.
        url = reverse('on_time_delivery_rate', args=[])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Vendor ID is required.'})
