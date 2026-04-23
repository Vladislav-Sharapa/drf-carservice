from typing import override

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin


from dealer.serializers.promotion import DealerPromotionCreateSerializer
from dealer.services.promotion import DealerPromotionService


class DealerPromotionCreateViewSet(GenericViewSet, CreateModelMixin):
    service = DealerPromotionService()
    serializer_class = DealerPromotionCreateSerializer

    @override
    def perform_create(self, serializer: DealerPromotionCreateSerializer):
        self.service.create(**serializer.validated_data)
