from django.contrib import admin

from core.models import CarModel
from supplier.models import Supplier

# Register your models here.
admin.site.register(Supplier)
admin.site.register(CarModel)
