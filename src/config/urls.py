from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from supplier.views import SupplierApiView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/", include("authentication.urls")),
    path("api/dealer/", include("dealer.urls")),
    path("api/supplier/", SupplierApiView.as_view()),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]
