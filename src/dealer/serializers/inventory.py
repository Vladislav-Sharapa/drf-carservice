from rest_framework.serializers import (
    IntegerField,
    Serializer,
    DecimalField,
    ModelSerializer,
)

from dealer.models import DealerShipInventory
from supplier.serializers.car import CarModelSerializer


class DealerInventoryUpdateSerializer(Serializer):
    min_required_stock = IntegerField(min_value=1, required=False)
    price = DecimalField(max_digits=10, decimal_places=2, min_value=1, required=False)


class DealerInventoryListSerializer(ModelSerializer):
    car = CarModelSerializer(many=False, required=False)

    class Meta:
        model = DealerShipInventory
        fields = "__all__"


class DealerInventoryCreateSerializer(ModelSerializer):
    class Meta:
        model = DealerShipInventory
        exclude = ["id", "created_at", "updated_at"]
