from typing import override

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)


from core.views import BaseGenericViewSet
from dealer.serializers.promotion import (
    DealerPromotionCreateSerializer,
    DealerPromotionListSerializer,
)
from dealer.services.promotion import DealerPromotionService


class DealerPromotionCreateViewSet(GenericViewSet, CreateModelMixin):
    service = DealerPromotionService()
    serializer_class = DealerPromotionCreateSerializer

    @override
    def perform_create(self, serializer: DealerPromotionCreateSerializer):
        self.service.create(**serializer.validated_data)


class DealerPromotionViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    BaseGenericViewSet,
):
    service = DealerPromotionService()
    queryset = service.get_all()
    serializer_class = DealerPromotionListSerializer

    serializer_map = {
        "create": DealerPromotionCreateSerializer,
    }
    serializer_map = {DealerPromotionCreateSerializer: ("create",)}

    @override
    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    @override
    def perform_create(self, serializer: DealerPromotionCreateSerializer):
        self.service.create(**serializer.validated_data)
