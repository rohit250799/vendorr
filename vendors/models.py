from django.db import models

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=60)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(unique=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()