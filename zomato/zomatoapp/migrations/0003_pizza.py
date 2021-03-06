# Generated by Django 3.1.2 on 2020-10-12 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zomatoapp', '0002_customer_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='pizzaimages/')),
                ('type', models.CharField(choices=[('veg', 'Veg'), ('nonveg', 'Non-veg')], max_length=50)),
                ('price', models.FloatField()),
            ],
        ),
    ]
