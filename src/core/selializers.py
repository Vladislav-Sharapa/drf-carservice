from rest_framework.serializers import ModelSerializer

from core.models import CarModel


class CarModelSerializer(ModelSerializer):
    class Meta:
        model = CarModel

        exclude = ["created_at", "updated_at"]
