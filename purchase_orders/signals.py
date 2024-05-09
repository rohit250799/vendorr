from django.db.models.signals import post_save
from django.dispatch import receiver
#from models import PurchaseOrders
#from vendors.models import Vendor
from django.db import models

purchase_order = models.ForeignKey('.PurchaseOrders', on_delete=models.CASCADE)

@receiver(post_save, sender=purchase_order)
def update_quality_rating_average(sender, instance, created, **kwargs):
    if created and instance.quality_rating is not None:
    #if created is not None and instance.quality_rating is not None or 
        vendor = instance.vendor
        print(vendor)
        completed_purchase_orders = vendor.purchaseorders_set.filter(
            delivery_date__isnull=False,
            status = 'COMPLETE',
            quality_rating__isnull = False
        )
        total_ratings = completed_purchase_orders.exclude(
            quality_rating__isnull=True,
            status = 'PENDING'
        ).count()
        total_ratings_sum = completed_purchase_orders.exclude(
            quality_rating__isnull=True
        ).aggregate(models.Sum('quality_rating'))['quality_rating__sum']
        if total_ratings > 0: average_rating = total_ratings_sum / total_ratings
        else: average_rating = None
        vendor.quality_rating_avg = average_rating
        vendor.save()



