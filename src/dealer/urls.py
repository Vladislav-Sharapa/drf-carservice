from django.urls import include, path
from rest_framework.routers import SimpleRouter

from dealer.views import DealerReqestCreateViewSet

router = SimpleRouter()

# Register routers
router.register("create", DealerReqestCreateViewSet, basename="dealer")

urlpatterns = [
    path("request/", include(router.urls)),
]
