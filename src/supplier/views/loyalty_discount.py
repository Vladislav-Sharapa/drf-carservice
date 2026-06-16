from typing import override

from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
)

from supplier.serializers.loyalty_discount import (
    SupplierLoyaltyDiscountCreateSerializer,
    SupplierLoyaltyDiscountListSerializer,
    SupplierLoyaltyDiscountUpdateSerializer,
)
from supplier.services.loyalty_discount import SupplierLoyaltyDiscountService


class SupplierLoyaltyDiscountViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
):
    service = SupplierLoyaltyDiscountService()
    queryset = service.get_all()
    serializer_class = SupplierLoyaltyDiscountListSerializer

    serializer_map = {
        "create": SupplierLoyaltyDiscountCreateSerializer,
        "update": SupplierLoyaltyDiscountUpdateSerializer,
    }

    @override
    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    @override
    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")
