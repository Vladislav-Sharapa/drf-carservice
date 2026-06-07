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
from dealer.views.dealership_stat import DealerShipStatViewSet


router = SimpleRouter()

router.register("", DealerShipViewSet, basename="dealership")
router.register("", DealerShipStatViewSet, basename="dealership_stat")
router.register("request", DealerRequestViewSet, basename="dealer-request")
router.register("inventory", DealerInventoryViewSet)
router.register("promotion", DealerPromotionViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
