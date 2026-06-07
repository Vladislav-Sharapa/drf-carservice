from http import HTTPMethod
from typing import override
from uuid import UUID

from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)

from dealer.serializers.dealer_request import DealerRequestListSerializer
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
        "sale_history": DealerRequestListSerializer,
    }

    @override
    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    @action(
        methods=[
            HTTPMethod.GET,
        ],
        detail=True,
        url_path="history",
    )
    def sale_history(self, request: Request, pk: UUID):
        requests = self.service.get_dealer_requests_by_supplier_id(pk)

        serializer = self.get_serializer(requests, many=True)

        return Response(serializer.data)
