# Generated by Django 3.1.2 on 2020-10-13 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zomatoapp', '0005_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zomatoapp.pizza'),
        ),
    ]