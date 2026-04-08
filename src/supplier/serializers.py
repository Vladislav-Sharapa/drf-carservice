from rest_framework import serializers
from supplier.models import Supplier


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "created_at"]