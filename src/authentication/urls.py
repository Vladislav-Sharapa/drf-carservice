from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import SimpleRouter
from authentication.views import UserViewSet

router = SimpleRouter()

# Register routers
router.register("account", UserViewSet, basename="user")

urlpatterns = [
    path("profile/", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
