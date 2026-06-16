from django.urls import include, path
from rest_framework.routers import SimpleRouter

from dealer.views.dealer_request import (
    # DealerReqeustCreateViewSet,
    # DealerRequestListViewSet,
    # DealerRequestUpdateViewSet,
    DealerRequestViewSet,
)
from dealer.views.dealership import DealerShipViewSet
from dealer.views.inventory import DealerInventoryViewSet
from dealer.views.promotion import DealerPromotionViewSet


router = SimpleRouter()

router.register("", DealerShipViewSet, basename="dealership")
router.register("request", DealerRequestViewSet, basename="dealer-request")
router.register("inventory", DealerInventoryViewSet)
# Dealer promotions routes
router.register("promotion", DealerPromotionViewSet)
# router.register(
#     "promotion", DealerPromotionListViewSet, basename="dealer-promotion-list"
# )


urlpatterns = [
    path("", include(router.urls)),
]
