from django.urls import include, path
from rest_framework.routers import SimpleRouter

from order.views import CustomerListViewSet


router = SimpleRouter()

# Register routers
router.register("list", CustomerListViewSet, basename="customer-list")

urlpatterns = [
    path("customer/", include(router.urls)),
]
