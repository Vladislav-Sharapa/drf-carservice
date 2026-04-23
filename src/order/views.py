from rest_framework.viewsets import ViewSet

from order.serializers.customer import CustomerSerializer
from order.services.customer import CustomerService
from rest_framework.request import Request
from rest_framework.response import Response


class CustomerListViewSet(ViewSet):
    user_service = CustomerService()
    serializer_class = CustomerSerializer

    def list(self, request: Request):
        data = self.user_service.get_all()
        serializer = self.serializer_class(data, many=True)

        return Response(serializer.data)
