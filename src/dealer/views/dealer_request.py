from uuid import uuid4

from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from http import HTTPMethod

from core.mixins.views import UpdateModelMixin
from dealer.flows.dealer_request import DealerRequestCreateFlow
from dealer.serializers.dealer_request import (
    DealerRequestCreateSerializer,
    DealerRequestListSerializer,
    DeaelerRequestUpdateSerializer,
)
from dealer.services.dealer_reqeust import DealerShipRequestService


class DealerReqeustCreateViewSet(ViewSet):
    service = DealerRequestCreateFlow()
    serializer_class = DealerRequestCreateSerializer

    def create(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.service.execute(**serializer.validated_data)
        return Response("detail: request is created")


class DealerRequestListViewSet(ViewSet):
    servise = DealerShipRequestService()
    serializer_class = DealerRequestListSerializer

    @action(
        detail=False,
        methods=[
            HTTPMethod.GET,
        ],
        url_path="dealership/(?P<dealership_id>[^/.]+)",
    )
    def list_by_dealer_id(self, request: Request, dealership_id: uuid4):
        instances = self.servise.get_by_dealer_id(dealership_id)

        serializer = self.serializer_class(instances, many=True)
        return Response(serializer.data)


class DealerRequestUpdateViewSet(ViewSet, UpdateModelMixin):
    service = DealerShipRequestService()
    serializer_class = DeaelerRequestUpdateSerializer

    def destroy(self, request: Request, pk: uuid4):
        request_db = self.service.get_pending_request_by_id(pk)
        self.service.delete(request_db.id)
