from rest_framework.serializers import ModelSerializer

from dealer.models import DealerShipPromotion


class DealerPromotionCreateSerializer(ModelSerializer):
    class Meta:
        model = DealerShipPromotion
        fields = "__all__"


class DealerPromotionListSerializer(ModelSerializer):
    class Meta:
        model = DealerShipPromotion
        fields = "__all__"
