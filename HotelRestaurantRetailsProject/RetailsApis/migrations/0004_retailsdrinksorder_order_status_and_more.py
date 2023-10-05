# Generated by Django 4.1.3 on 2023-09-29 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RetailsApis', '0003_retailsproductsunit_retailsdrinksproducts_unit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='retailsdrinksorder',
            name='order_status',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='retailsdrinksorderitems',
            name='order_status',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='retailsfoodorder',
            name='order_status',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='retailsfoodorderitems',
            name='order_status',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Status'),
        ),
    ]