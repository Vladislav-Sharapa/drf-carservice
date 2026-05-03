from rest_framework.serializers import ModelSerializer

from supplier.models import CarModel


class CarModelSerializer(ModelSerializer):
    class Meta:
        model = CarModel
        exclude = ["created_at", "updated_at"]


class CarModelCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = CarModel
        exclude = ["id", "created_at", "updated_at"]
