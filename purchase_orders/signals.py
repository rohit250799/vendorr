from django.db.models.signals import post_save
from django.dispatch import receiver
#from models import PurchaseOrders
#from vendors.models import Vendor
from django.db import models

purchase_order = models.ForeignKey('.PurchaseOrders', on_delete=models.CASCADE)

@receiver(post_save, sender=purchase_order)
def update_quality_rating_average(sender, instance, created, **kwargs):
    if instance.status == 'COMPLETE' and instance.quality_rating is not None:
        vendor = instance.vendor
        completed_purchase_orders = vendor.purchaseorders_set.filter(
            status = 'COMPLETE',
            quality_rating__isnull = False
        )
        total_ratings = completed_purchase_orders.count()
        total_ratings_sum = completed_purchase_orders.aggregate(
            models.Sum('quality_rating')
        )['quality_rating__sum']
        if total_ratings > 0: average_rating = total_ratings_sum / total_ratings
        else: average_rating = None
        vendor.quality_rating_avg = average_rating
        vendor.save()


@receiver(post_save, sender=purchase_order)
def update_average_response_time(sender, instance, created, **kwargs):
    if created and instance.acknowledgement_date:
        vendor = instance.vendor
        total_response_time = vendor.total_response_time + (
            instance.acknowledgement_date - instance.issue_date
        ).total_seconds()
        total_purchase_orders_acknowledged = vendor.purchaseorder_set.filter(
            acknowledgement_date__isnull=False
        ).count()
        vendor.average_response_time = total_response_time / total_purchase_orders_acknowledged
        vendor.save()