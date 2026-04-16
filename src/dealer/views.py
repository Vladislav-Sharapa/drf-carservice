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
            self.service.execute(
                dealer_id=serializer.validated_data["dealer_id"],
                car_id=serializer.validated_data["car_id"],
                count=serializer.validated_data["count"],
            )
        return Response("detail: request is created")
