from django.contrib import admin

from supplier.models import (
    CarModel,
    Supplier,
    SupplierLoyaltyDiscount,
    SupplierInventory,
    SupplierPromotion,
)

# Register your models here.
admin.site.register(Supplier)
admin.site.register(CarModel)
admin.site.register(SupplierLoyaltyDiscount)
admin.site.register(SupplierInventory)
admin.site.register(SupplierPromotion)
