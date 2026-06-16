from typing import override

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)

from supplier.serializers.inventory import (
    SupplierInventoryCreateSerializer,
    SupplierInventoryListSerializer,
    SupplierInventoryUpdateSerializer,
)
from supplier.services.inventory import SupplierInventoryService


class SupplierInventoryViewSet(
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    service = SupplierInventoryService()
    queryset = service.get_all()
    serializer_class = SupplierInventoryListSerializer

    serializer_map = {
        "create": SupplierInventoryCreateSerializer,
        "update": SupplierInventoryUpdateSerializer,
        "partial_update": SupplierInventoryUpdateSerializer,
    }

    @override
    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)
