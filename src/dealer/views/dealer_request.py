from uuid import UUID

from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response

from core.mixins.views import UpdateModelMixin
from dealer.flows.dealer_request import DealerRequestCreateFlow
from dealer.serializers.dealer_request import (
    DealerRequestCreateSerializer,
    DealerRequestListSerializer,
    DeaelerRequestUpdateSerializer,
)
from dealer.services.dealer_reqeust import DealerShipRequestService
from typing import override


class DealerRequestViewSet(GenericViewSet, UpdateModelMixin):
    service = DealerShipRequestService()
    dealer_flow = DealerRequestCreateFlow()

    @override
    def get_serializer_class(self):
        if self.action == "create":
            return DealerRequestCreateSerializer
        elif self.action in ("retrieve", "list_by_dealer_id"):
            return DealerRequestListSerializer
        elif self.action in ("update", "destroy"):
            return DeaelerRequestUpdateSerializer

        return super().get_serializer_class()

    def create(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.dealer_flow.execute(**serializer.validated_data)
        return Response("detail: request is created")

    def retrieve(self, request: Request, pk: UUID = None):
        instance = self.service.get_by_id(pk)
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def destroy(self, request: Request, pk: UUID):
        request_db = self.service.get_pending_request_by_id(pk)
        self.service.delete(request_db.id)
