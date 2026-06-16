from django.contrib import admin

from order.models import CustomerProfile, Order

# Register your models here.
admin.site.register(CustomerProfile)
admin.site.register(Order)
