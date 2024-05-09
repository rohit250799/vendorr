from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import PurchaseOrders
from vendors.models import Vendor

#for the signal handler
from django.db.models.signals import post_save
from django.test.utils import override_settings
from django.core import management
from vendors.models import Vendor
from .signals import update_quality_rating_average

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
            on_time_delivery_rate = 51,
            quality_rating_avg = 34.4,
            average_response_time = 58,
            fulfillment_rate = 49.9,
        )

    def test_on_time_delivery_rate_no_completed_orders(self):
        #Testing on time delivery rate custom action with 0 completed purchase orders
        url = reverse('on_time_delivery_rate', args=[self.vendor.id])
        response = self.client.get(url)
        order_date = "2012-3-21", 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['on_time_delivery_rate'], 0)

    def test_on_time_delivery_rate_with_completed_orders(self):
        #Testing on time delivery rate custom action with completed purchase orders
        on_time_purchase_order = PurchaseOrders.objects.create(
            vendor=self.vendor,
            po_number = 2900,
            order_date = "2012-3-21",
            items = {
                "title": "water bottle",
                "itemId": 1,
                "completed": True,
            },
            quantity = 14,
            status="DONE",
            delivery_date=timezone.now() + timezone.timedelta(days=5),
        )

        late_purchase_order = PurchaseOrders.objects.create(
            vendor=self.vendor,
            po_number = 223,
            order_date = "2012-3-21",
            items = {
                "title": "water bottle",
                "itemId": 1,
                "completed": True,
            },
            quantity = 25,
            status="DONE",
            delivery_date=timezone.now() + timezone.timedelta(days=5),
        )

        url = reverse('on_time_delivery_rate', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['on_time_delivery_rate'], 50.0)

    def test_on_time_delivery_rate_invalid_vendor_id(self):
        #Test the on_time_delivery_rate custom action with an invalid vendor ID.
        url = reverse('on_time_delivery_rate', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Vendor ID is required.'})

#testing the signal handler is working
class SignalHandlerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Connect the signal handler
        post_save.connect(update_quality_rating_average, sender=PurchaseOrders)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Disconnect the signal handler
        post_save.disconnect(update_quality_rating_average, sender=PurchaseOrders)

    def setUp(self):
        # Create some test data
        self.vendor = Vendor.objects.create(name='Test Vendor')
        self.purchase_order1 = PurchaseOrders.objects.create(vendor=self.vendor, po_number=23, order_date="2012-3-21", delivery_date="2012-4-11", items={"title": "water bottle", "itemId": 1, "completed": True}, quantity = 25, status='COMPLETE', quality_rating=4)
        self.purchase_order2 = PurchaseOrders.objects.create(vendor=self.vendor, po_number=17, order_date="2012-3-21", delivery_date="2012-4-11", items={"title": "drink bottle", "itemId": 2, "completed": True}, quantity = 25, status='COMPLETE', quality_rating=3)

    def test_quality_rating_avg_updated(self):
        # Check initial quality_rating_avg
        self.assertEqual(self.vendor.quality_rating_avg, 3.5)  # Average of 4 and 3

        # Create a new completed purchase order with a quality rating
        purchase_order = PurchaseOrders.objects.create(vendor=self.vendor, po_number=45, order_date="2012-3-21", delivery_date="2012-4-11", items={"title": "apple", "itemId": 3, "completed": True}, quantity = 35,status='COMPLETE', quality_rating=5)

        # Refresh the vendor object from the database to get the updated value
        self.vendor.refresh_from_db()

        # Check if quality_rating_avg is updated correctly
        self.assertEqual(self.vendor.quality_rating_avg, 4)  # New average of 4, 3, and 5

