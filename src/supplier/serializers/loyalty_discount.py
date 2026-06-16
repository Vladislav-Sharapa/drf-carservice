from dealer.serializers.dealership import DealerShipListSerializer
from supplier.models import SupplierLoyaltyDiscount
from rest_framework.serializers import ModelSerializer

from supplier.serializers.supplier import SupplierListSerializer


class SupplierLoyaltyDiscountListSerializer(ModelSerializer):
    supplier = SupplierListSerializer(many=False, required=False)
    dealership = DealerShipListSerializer(many=False, required=False)

    class Meta:
        model = SupplierLoyaltyDiscount
        exclude = ["created_at", "updated_at"]


class SupplierLoyaltyDiscountCreateSerializer(ModelSerializer):
    class Meta:
        model = SupplierLoyaltyDiscount
        exclude = ["id", "created_at", "updated_at"]


class SupplierLoyaltyDiscountUpdateSerializer(ModelSerializer):
    class Meta:
        model = SupplierLoyaltyDiscount
        fields = ["discount_percent"]
