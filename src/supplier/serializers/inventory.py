from rest_framework.serializers import ModelSerializer

from supplier.models import SupplierInventory


class SupplierInventoryListSerializer(ModelSerializer):
    class Meta:
        model = SupplierInventory
        fields = "__all__"


class SupplierInventoryCreateSerializer(ModelSerializer):
    class Meta:
        model = SupplierInventory
        exclude = ["id", "created_at", "updated_at"]


class SupplierInventoryUpdateSerializer(ModelSerializer):
    class Meta:
        model = SupplierInventory
        fields = [
            "price",
        ]
