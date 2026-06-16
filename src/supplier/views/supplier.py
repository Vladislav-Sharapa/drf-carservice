from typing import override

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)

from supplier.serializers.supplier import (
    SupplierCreateUpdateSerializer,
    SupplierListSerializer,
)
from supplier.services.supplier import SupplierService


class SupplierViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
):
    service = SupplierService()
    queryset = service.get_all()
    serializer_class = SupplierListSerializer

    serializer_map = {
        "create": SupplierCreateUpdateSerializer,
        "update": SupplierCreateUpdateSerializer,
    }

    @override
    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)
