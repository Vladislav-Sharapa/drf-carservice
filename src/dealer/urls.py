from django.urls import include, path
from rest_framework.routers import SimpleRouter

from dealer.views.dealer_request import (
    DealerReqeustCreateViewSet,
    DealerRequestListViewSet,
    DealerRequestUpdateViewSet,
)
from dealer.views.inventory import DealerInventoryUpdateViewSet
from dealer.views.promotion import (
    DealerPromotionCreateViewSet,
    DealerPromotionListViewSet,
)


router = SimpleRouter()

# Dealer request routes
router.register("request/create", DealerReqeustCreateViewSet, basename="dealer-request")
router.register(
    "request/list", DealerRequestListViewSet, basename="dealer-request-list"
)
router.register(
    "request/update", DealerRequestUpdateViewSet, basename="dealer-request-update"
)
# Dealer inventory routes
router.register(
    "inventory/update", DealerInventoryUpdateViewSet, basename="dealer-inventory-update"
)
# Dealer promotions routes
router.register(
    "promotion/create", DealerPromotionCreateViewSet, basename="dealer-promotion-create"
)
router.register(
    "promotion", DealerPromotionListViewSet, basename="dealer-promotion-list"
)


urlpatterns = [
    path("", include(router.urls)),
]
