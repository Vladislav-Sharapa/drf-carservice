from django.contrib import admin
from django.urls import include, path
from supplier.views import SupplierApiView
from supplier import urls as supplier_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/v1/supplier/", SupplierApiView.as_view())
]
