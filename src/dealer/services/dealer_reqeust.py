from typing import Sequence
from uuid import uuid4

from core.enums import TransactionStatusEnum
from core.models import CarModel
from core.services import BaseService
from dealer.models import DealerShip, DealerShipRequest
from supplier.models import Supplier
from rest_framework.exceptions import NotFound


class DealerShipRequestService(BaseService):
    model = DealerShipRequest

    def get(self, dealer_id: uuid4, car_id: uuid4) -> DealerShipRequest:
        instance = DealerShipRequest.objects.filter(
            dealer_id=dealer_id, car_id=car_id
        ).select_related("car", "dealership")
        if not instance:
            raise NotFound
        return instance

    def get_by_dealer_id(self, dealer_id: uuid4) -> Sequence:
        request = self.model.objects.filter(dealership_id=dealer_id).select_related(
            "car"
        )

        if not request:
            raise NotFound(
                detail=f"There is no dealership requsts with dealearhip id:{dealer_id}"
            )
        return request

    def get_pending_request_by_id(self, id: uuid4):
        request = DealerShipRequest.objects.filter(
            id=id, status=TransactionStatusEnum.PENDING
        )
        if not request:
            raise NotFound
        return request

    def get_by_status(self, status) -> Sequence:
        requests = DealerShipRequest.objects.filter(status=status)
        if not requests.exists():
            return []
        return requests

    def deploy_request(
        self, dealership: DealerShip, car: CarModel, count: int
    ) -> DealerShipRequest:
        return DealerShipRequest.objects.create(
            dealership=dealership,
            car=car,
            status=TransactionStatusEnum.PENDING,
            count=count,
        )

    def set_supplier(self, request_id: uuid4, supplier: Supplier) -> None:
        request = self.get_pending_request_by_id(request_id)
        request.supplier = supplier

        request.save()

    def set_status(self, request_id: uuid4, status: str) -> None:
        request = self.get_pending_request_by_id(request_id)
        request.status = status

        request.save()

    def set_error(self, request_id: uuid4, error_description: str) -> None:
        request = self.get_pending_request_by_id(request_id)
        request.error_description = error_description
        request.status = TransactionStatusEnum.ERROR

        request.save()
