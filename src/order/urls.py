from django.urls import include, path
from rest_framework.routers import SimpleRouter

from order.views.customer import CustomerListViewSet
from order.views.order import OrderViewSet


customer_router = SimpleRouter()
order_router = SimpleRouter()

# Register routers
customer_router.register("", CustomerListViewSet)
order_router.register("", OrderViewSet)

urlpatterns = [
    path("customer", include(customer_router.urls)),
    path("order", include(order_router.urls)),
]
