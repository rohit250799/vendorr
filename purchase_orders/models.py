from django.db import models
from django.utils.translation import gettext_lazy as _
from vendors.models import Vendor as VendorModel

# Create your models here.
class PurchaseOrders(models.Model):
    class PurchaseOrderStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        COMPLETED = "COMPLETE", _("Completed")
        CANCELLED = "CANCEL", _("Cancelled")

    po_number = models.CharField(unique=True)
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(
        max_length=8, choices=PurchaseOrderStatus,
        default=PurchaseOrderStatus.PENDING
    )
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now=True)
    acknowledgement_date = models.DateTimeField(null=True, auto_now_add=True)