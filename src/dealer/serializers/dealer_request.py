from rest_framework.serializers import (
    IntegerField,
    Serializer,
    ModelSerializer,
    ChoiceField,
    UUIDField,
    CharField,
)

from core.enums import TransactionStatusEnum
from core.selializers import CarModelSerializer
from dealer.models import DealerShipRequest


class DealerRequestCreateSerializer(Serializer):
    count = IntegerField(min_value=1)
    car_id = IntegerField(min_value=1)
    dealer_id = IntegerField(min_value=1)


class DeaelerRequestUpdateSerializer(Serializer):
    status = ChoiceField(choices=TransactionStatusEnum.choices, required=False)
    count = IntegerField(min_value=1, required=False)
    supplier_id = UUIDField(required=False)
    error_description = CharField(max_length=200, required=False)


class DealerRequestListSerializer(ModelSerializer):
    car = CarModelSerializer(many=False, required=False)

    class Meta:
        model = DealerShipRequest

        fields = ["id", "status", "count", "car"]
