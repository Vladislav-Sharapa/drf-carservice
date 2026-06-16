from typing import override

from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
)

from core.views import BaseGenericViewSet
from dealer.serializers.inventory import (
    DealerInventoryCreateSerializer,
    DealerInventoryListSerializer,
    DealerInventoryUpdateSerializer,
)
from dealer.services.inventory import DealerShipInventoryService


class DealerInventoryViewSet(
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    BaseGenericViewSet,
):
    service = DealerShipInventoryService()
    queryset = service.get_all()
    serializer_class = DealerInventoryListSerializer

    serializer_map = {
        DealerInventoryCreateSerializer: ("create",),
        DealerInventoryUpdateSerializer: ("update",),
    }

    @override
    def get_queryset(self):
        if self.action == "list":
            return self.service.list()

        return super().get_queryset()
