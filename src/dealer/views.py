from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response

from dealer.flows.dealer_request import DealerRequestCreateFlow
from dealer.serializers.dealer_request import DealerRequestCreateSerializer


class DealerReqestCreateViewSet(ViewSet):
    service = DealerRequestCreateFlow()

    def create(self, request: Request):
        serializer = DealerRequestCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.service.execute(**serializer.validated_data)
        return Response("detail: request is created")
