from rest_framework.serializers import IntegerField, Serializer


class DealerRequestCreateSerializer(Serializer):
    count = IntegerField(min_value=1)
    car_id = IntegerField(min_value=1)
    dealer_id = IntegerField(min_value=1)


class DealerRequestOutputSerializer(Serializer):
    pass
