from rest_framework.serializers import (
    IntegerField,
    Serializer,
    ModelSerializer,
    ChoiceField,
    UUIDField,
    CharField,
)

from core.enums import TransactionStatusEnum
from dealer.models import DealerShipRequest
from supplier.serializers.car import CarModelSerializer


class DealerRequestCreateSerializer(Serializer):
    quantity = IntegerField(min_value=1)
    car_id = UUIDField()
    dealer_id = UUIDField()


class DeaelerRequestUpdateSerializer(Serializer):
    status = ChoiceField(choices=TransactionStatusEnum.choices, required=False)
    quantity = IntegerField(min_value=1, required=False)
    supplier_id = UUIDField(required=False)
    error_description = CharField(max_length=200, required=False)


class DealerRequestListSerializer(ModelSerializer):
    car = CarModelSerializer(many=False, required=False)

    class Meta:
        model = DealerShipRequest

        exclude = ["supplier"]


class DealerRequestFilterSerializer(Serializer):
    status = CharField(required=False)
    car_id = UUIDField(required=False)
