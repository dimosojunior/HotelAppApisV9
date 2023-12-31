# Generated by Django 4.1.3 on 2023-10-03 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RetailsApis', '0006_retailstables_retailsdrinkscartitems_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='retailsdrinkscartitems',
            name='CustomerAddress',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Customer Address'),
        ),
        migrations.AddField(
            model_name='retailsdrinkscartitems',
            name='CustomerFullName',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Customer Full Name'),
        ),
        migrations.AddField(
            model_name='retailsdrinkscartitems',
            name='PhoneNumber',
            field=models.CharField(blank=True, default='+255', max_length=14, null=True, verbose_name='Phone Number'),
        ),
        migrations.AddField(
            model_name='retailsdrinksorderitems',
            name='CustomerAddress',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Customer Address'),
        ),
        migrations.AddField(
            model_name='retailsdrinksorderitems',
            name='CustomerFullName',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Customer Full Name'),
        ),
        migrations.AddField(
            model_name='retailsdrinksorderitems',
            name='PhoneNumber',
            field=models.CharField(blank=True, default='+255', max_length=14, null=True, verbose_name='Phone Number'),
        ),
        migrations.AddField(
            model_name='retailsfoodcartitems',
            name='CustomerAddress',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Customer Address'),
        ),
        migrations.AddField(
            model_name='retailsfoodcartitems',
            name='CustomerFullName',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Customer Full Name'),
        ),
        migrations.AddField(
            model_name='retailsfoodcartitems',
            name='PhoneNumber',
            field=models.CharField(blank=True, default='+255', max_length=14, null=True, verbose_name='Phone Number'),
        ),
        migrations.AddField(
            model_name='retailsfoodorderitems',
            name='CustomerAddress',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Customer Address'),
        ),
        migrations.AddField(
            model_name='retailsfoodorderitems',
            name='CustomerFullName',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Customer Full Name'),
        ),
        migrations.AddField(
            model_name='retailsfoodorderitems',
            name='PhoneNumber',
            field=models.CharField(blank=True, default='+255', max_length=14, null=True, verbose_name='Phone Number'),
        ),
    ]
