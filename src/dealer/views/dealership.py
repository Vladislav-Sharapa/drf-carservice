from http import HTTPMethod
from uuid import UUID

from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from typing import Sequence

from core.views import BaseGenericViewSet
from dealer.models import DealerShipInventory, DealerShipRequest
from dealer.serializers.dealer_request import (
    DealerRequestFilterSerializer,
    DealerRequestListSerializer,
)
from dealer.serializers.dealership import DealerShipListSerializer
from dealer.serializers.inventory import DealerInventoryListSerializer
from dealer.serializers.promotion import DealerPromotionListSerializer
from dealer.services.dealership import DealerShipService
from supplier.serializers.loyalty_discount import SupplierLoyaltyDiscountListSerializer


class DealerShipViewSet(ListModelMixin, BaseGenericViewSet):
    service = DealerShipService()
    queryset = service.get_all()
    serializer_class = DealerShipListSerializer

    serializer_map = {
        DealerRequestListSerializer: ("request",),
        DealerInventoryListSerializer: ("inventory",),
        DealerPromotionListSerializer: ("promotions",),
        SupplierLoyaltyDiscountListSerializer: ("loyalty_discount",),
    }

    @action(
        methods=[
            HTTPMethod.GET,
        ],
        detail=True,
        url_path="requests",
    )
    def requests(
        self, request: Request, pk: UUID = None
    ) -> Sequence[DealerShipRequest]:
        filters_serializer = DealerRequestFilterSerializer(data=request.query_params)
        if filters_serializer.is_valid():
            filters = filters_serializer.validated_data
        else:
            filters = None
        requests = self.service.get_requests(pk, filters)

        return self._get_response_list(requests)

    @action(
        methods=[
            HTTPMethod.GET,
        ],
        detail=True,
        url_path="inventory",
    )
    def inventory(
        self, request: Request, pk: UUID = None
    ) -> Sequence[DealerShipInventory]:
        inventory = self.service.get_inventory(pk)

        return self._get_response_list(inventory)

    @action(
        methods=[
            HTTPMethod.GET,
        ],
        detail=True,
        url_path="promotions",
    )
    def promotions(self, requset: Request, pk: UUID = None):
        promotions = self.service.get_promotions(pk)

        return self._get_response_list(promotions)

    @action(
        methods=[
            HTTPMethod.GET,
        ],
        detail=True,
        url_path="discount",
    )
    def loyalty_discount(self, request: Request, pk: UUID = None):
        discount = self.service.get_loyalty_discount(pk)

        return self._get_response_list(discount)

    def _get_response_list(self, items: Sequence):
        serializer = self.get_serializer(items, many=True)

        return Response(serializer.data)
