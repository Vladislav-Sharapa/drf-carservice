from rest_framework.serializers import ModelSerializer

from dealer.models import DealerShip


class DealerShipListSerializer(ModelSerializer):
    class Meta:
        model = DealerShip
        fields = "__all__"
