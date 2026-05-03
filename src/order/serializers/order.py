from rest_framework.serializers import ModelSerializer

from order.models import Order


class OrderListSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderCreateSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "car",
        ]
