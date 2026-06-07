from http import HTTPMethod
from uuid import UUID

from django_filters.rest_framework import DjangoFilterBackend

from core.enums import TransactionStatusEnum
from core.views import BaseGenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.request import Request
from rest_framework.response import Response

from dealer.filters import OrderFilter
from dealer.serializers.dealership import DealerShipListSerializer
from dealer.services.dealership import DealerShipService
from order.serializers.order import OrderListSerializer
from order.services.order import OrderService


class DealerShipStatViewSet(ListModelMixin, BaseGenericViewSet):
    service = DealerShipService()
    queryset = service.get_all()
    serializer_class = DealerShipListSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilter

    serializer_map = {OrderListSerializer: ("history",)}

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="start_date",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description="Start date (YYYY-MM-DD)",
                required=False,
            ),
            OpenApiParameter(
                name="end_date",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description="End date (YYYY-MM-DD)",
                required=False,
            ),
            OpenApiParameter(
                name="status",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Order status",
                required=False,
                enum=[choice[0] for choice in TransactionStatusEnum.choices],
            ),
        ],
        responses={200: OrderListSerializer(many=True)},
    )
    @action(
        methods=[
            HTTPMethod.GET,
        ],
        detail=True,
        url_path="history",
    )
    def history(self, request: Request, pk: UUID = None):
        queryset = self.service.get_orders(pk)
        orders = self.filter_queryset(queryset)

        serializer = self.get_serializer(orders, many=True)

        return Response(serializer.data)

    @action(
        methods=[
            HTTPMethod.GET,
        ],
        detail=True,
        url_path="total",
    )
    def total(self, request: Request, pk: UUID = None):
        order_service = OrderService()
        queryset = self.service.get_orders(pk)
        orders = self.filter_queryset(queryset)

        result = order_service.get_completed_orders_income(orders)

        return Response(result)
