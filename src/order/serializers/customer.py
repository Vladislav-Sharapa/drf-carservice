from rest_framework.serializers import ModelSerializer

from authentication.serializers import UserSerializer
from order.models import CustomerProfile


class CustomerSerializer(ModelSerializer):
    user = UserSerializer(many=False, required=False)

    class Meta:
        model = CustomerProfile
        exclude = ["created_at", "updated_at"]
