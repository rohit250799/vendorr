from django.db import models

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=60)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)


    def update_quality_rating_avg(self):
        completed_purchase_orders = self.purchaseorder_set.filter(
            status = 'COMPLETE',
            quality_rating__isnull=False
        )
        if completed_purchase_orders.exists():
            total_ratings = sum(
                purchaseorders.quality_rating for purchaseorders in completed_purchase_orders)
            self.quality_rating_avg = total_ratings / completed_purchase_orders.count()
        else: self.quality_rating_avg = 0.0
        self.save()

class HistoricalPerformances(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
