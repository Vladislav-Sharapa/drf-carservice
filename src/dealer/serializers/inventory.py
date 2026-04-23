from rest_framework.serializers import IntegerField, Serializer, DecimalField


class DealerInventoryUpdateSerializer(Serializer):
    min_required_stock = IntegerField(min_value=1, required=False)
    price = DecimalField(max_digits=10, decimal_places=2, min_value=1, required=False)
