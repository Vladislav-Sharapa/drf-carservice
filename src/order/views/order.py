from http import HTTPMethod
from typing import override

from core.views import BaseGenericViewSet
from dealer.flows.dealer_request import DealerRequestProcessFlow
from dealer.serializers.dealer_request import DealerRequestListSerializer
from dealer.services.dealer_reqeust import DealerShipRequestService
from order.flows.order import OrderProcessingFlow
from order.serializers.order import OrderCreateSerializer, OrderListSerializer
from order.services.customer import CustomerService
from order.services.order import OrderService
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.serializers import Serializer
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response


class OrderViewSet(ListModelMixin, CreateModelMixin, BaseGenericViewSet):
    service = OrderService()
    queryset = service.get_all()
    serializer_class = OrderListSerializer
    permission_classes = (IsAuthenticated,)

    serializer_map = {
        OrderCreateSerializer: ("create",),
        DealerRequestListSerializer: ("proc",),
    }

    @override
    def perform_create(self, serializer: Serializer):
        service = CustomerService()
        car_id = serializer.validated_data["car"]
        user = self.request.user
        if isinstance(user, AnonymousUser):
            raise APIException(detail="Login before creating order")
        customer = service.get_by_user_id(user_id=user.id)

        self.service.create(car_id=car_id, customer_id=customer.id)

    @action(
        methods=[
            HTTPMethod.POST,
        ],
        detail=False,
        url_path="process",
    )
    def process(self, request: Request):
        order = self.service.get_by_id("4b2bc364-3938-41f3-885d-83e8614fed33")
        serv = OrderProcessingFlow()
        order = serv.execute(order)
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(
        methods=[
            HTTPMethod.POST,
        ],
        detail=False,
        url_path="proc",
    )
    def proc(self, request):
        service = DealerShipRequestService()
        request = service.get_by_id("f3b3e1cc-d0cb-4f59-b6e7-c207f8e43ad1")
        serv = DealerRequestProcessFlow()
        request = serv.execute(request)
        serializer = self.get_serializer(request)
        return Response(serializer.data)
