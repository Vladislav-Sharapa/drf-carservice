from uuid import uuid4

from core.services import CarService
from dealer.services.dealer_reqeust import DealerShipRequestService
from dealer.services.dealership import DealerShipService
from rest_framework.exceptions import APIException
from rest_framework import status
from django.db import transaction


class DealerRequestCreateFlow:
    def __init__(self):
        self.dealer_request_service = DealerShipRequestService()
        self.dealership_service = DealerShipService()
        self.car_service = CarService()

    @transaction.atomic
    def execute(self, dealer_id: uuid4, car_id: uuid4, count: int):
        dealership = self.dealership_service.get_by_id(dealer_id)
        car = self.car_service.get_by_id(car_id)

        try:
            response = self.dealer_request_service.deploy_request(
                dealership=dealership, car=car, count=count
            )
        except Exception as e:
            raise APIException(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error during processing data. Detail: {e}",
            )

        return response
