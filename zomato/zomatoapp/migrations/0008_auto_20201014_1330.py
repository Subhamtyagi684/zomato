# Generated by Django 3.1.2 on 2020-10-14 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zomatoapp', '0007_order_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]