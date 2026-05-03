from django.urls import include, path
from rest_framework.routers import SimpleRouter

from supplier.views.car import CarViewSet
from supplier.views.inventory import SupplierInventoryViewSet
from supplier.views.loyalty_discount import SupplierLoyaltyDiscountViewSet
from supplier.views.supplier import SupplierViewSet

supplier_router = SimpleRouter()
car_router = SimpleRouter()

supplier_router.register("", SupplierViewSet)
supplier_router.register("loyalty/discount", SupplierLoyaltyDiscountViewSet)
supplier_router.register("inventory", SupplierInventoryViewSet)

car_router.register("", CarViewSet)

urlpatterns = [
    path("supplier/", include(supplier_router.urls)),
    path("car/", include(car_router.urls)),
]
