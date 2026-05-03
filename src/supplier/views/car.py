from django_filters.rest_framework import DjangoFilterBackend

from core.views import BaseGenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin

from supplier.filters import CarFilter
from supplier.serializers.car import CarModelCreateUpdateSerializer, CarModelSerializer
from supplier.services.car import CarService


class CarViewSet(
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, BaseGenericViewSet
):
    service = CarService()
    queryset = service.get_all()
    serializer_class = CarModelSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarFilter

    serializer_map = {CarModelCreateUpdateSerializer: ("update", "partial_update")}
