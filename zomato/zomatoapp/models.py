from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer (models.Model):
    fullname = models.CharField(max_length=50)
    email= models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.fullname


class Pizza(models.Model):
    name= models.CharField(max_length=100)
    image = models.ImageField(upload_to='pizzaimages/',unique=True)
    type = models.CharField(max_length=50,choices=(
        ('veg','Veg'),
        ('nonveg','Non-veg'),
    ))
    price = models.FloatField()

    def __str__(self):
        return self.name


class Order(models.Model):
    cust_name = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_name = models.ForeignKey(Pizza,on_delete=models.CASCADE)
    quantity = models.CharField(default=1,max_length=100)

