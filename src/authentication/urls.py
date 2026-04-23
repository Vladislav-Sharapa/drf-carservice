from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import SimpleRouter
from authentication.views import UserCreateViewSet

router = SimpleRouter()

# Register routers
router.register("create", UserCreateViewSet, basename="user-create")

urlpatterns = [
    path("account/", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
