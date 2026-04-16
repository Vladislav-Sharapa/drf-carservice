from typing import Sequence
import uuid

from core.enums import TransactionStatusEnum
from core.models import CarModel
from core.services import BaseService
from dealer.exceptions import NotPendingReqestException
from dealer.models import DealerShip, DealerShipRequest
from supplier.models import Supplier
from rest_framework.exceptions import NotFound


class DealerShipRequestService(BaseService):
    model = DealerShipRequest

    def get_pending_request_by_id(self, id: uuid):
        request = self.get_by_id(id)
        if request.status in (
            TransactionStatusEnum.ERROR,
            TransactionStatusEnum.FAILED,
        ):
            raise NotPendingReqestException(
                detail=f"Request must have status PENDING or PROCESSING. The requested one is {request.status}"
            )
        return request

    def get_by_status(self, status) -> Sequence[DealerShipRequest] | None:
        requests = DealerShipRequest.objects.filter(status=status)
        if not requests.exists():
            raise NotFound
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

    def set_supplier(self, request_id: uuid, supplier: Supplier) -> None:
        request = self.get_pending_request_by_id(request_id)
        request.supplier = supplier

        request.save()

    def set_status(self, request_id: uuid, status: str) -> None:
        request = self.get_pending_request_by_id(request_id)
        request.status = status

        request.save()

    def set_error(self, request_id: uuid, error_description: str) -> None:
        request = self.get_pending_request_by_id(request_id)
        request.error_description = error_description
        request.status = TransactionStatusEnum.ERROR

        request.save()
