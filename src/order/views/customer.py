from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from core.views import BaseGenericViewSet
from order.serializers.customer import CustomerSerializer
from order.services.customer import CustomerService


class CustomerListViewSet(ListModelMixin, RetrieveModelMixin, BaseGenericViewSet):
    service = CustomerService()
    serializer_class = CustomerSerializer
    queryset = service.get_all()
