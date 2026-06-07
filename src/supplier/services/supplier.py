from uuid import UUID

from core.services import BaseService
from dealer.models import DealerShipRequest
from supplier.models import Supplier

from rest_framework.exceptions import NotFound


class SupplierService(BaseService):
    model = Supplier

    def get_dealer_requests_by_supplier_id(self, pk: UUID):
        requests = DealerShipRequest.objects.filter(supplier_id=pk).select_related(
            "car"
        )

        if not requests:
            raise NotFound
        return requests
