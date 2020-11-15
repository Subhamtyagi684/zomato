from django.contrib import admin
from .models import Customer,Pizza, Order
# Register your models here.

admin.site.register(Customer)
admin.site.register(Pizza)
admin.site.register(Order)