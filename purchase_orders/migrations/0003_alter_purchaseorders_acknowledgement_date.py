# Generated by Django 5.0.4 on 2024-05-12 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_orders', '0002_alter_purchaseorders_quality_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorders',
            name='acknowledgement_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
