from rest_framework.serializers import ModelSerializer

from supplier.models import Supplier


class SupplierListSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class SupplierCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ["id"]
