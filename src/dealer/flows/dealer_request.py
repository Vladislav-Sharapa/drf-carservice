from decimal import Decimal
from uuid import uuid4

from core.enums import TransactionStatusEnum
from core.services import CarService
from dealer.exceptions import NegativeBalanceException
from dealer.models import DealerShip, DealerShipRequest
from dealer.services.dealer_reqeust import DealerShipRequestService
from dealer.services.dealership import DealerShipService
from rest_framework.exceptions import APIException
from django.db import transaction

from dealer.services.inventory import DealerShipInventoryService
from supplier.services.inventory import SupplierInventoryService


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
                detail=f"Error during processing data. Detail: {e}",
            )

        return response


class DealerRequestProcessFlow:
    def __init__(self):
        self.dealer_inventory_service = DealerShipInventoryService()
        self.dealer_request_serice = DealerShipRequestService()
        self.dealership_service = DealerShipService()
        self.supplier_inventory_service = SupplierInventoryService()

    @transaction.atomic
    def execute(
        self, dealer_id: uuid4, car_id: uuid4, request_id: uuid4, supplier_id: uuid4
    ):
        """Executes a dealership transaction for purchasing a car from a supplier."""
        dealer_inventory = self.dealer_inventory_service.get(
            dealer_id=dealer_id, car_id=car_id
        )
        supplier_inventory = self.supplier_inventory_service.get(
            supplier_id=supplier_id, car_id=car_id
        )
        dealer_request: DealerShipRequest = self.dealer_request_serice.get_by_id(
            request_id
        )
        dealership: DealerShip = self.dealership_service.get_by_id(dealer_id)

        try:
            new_balance = self.__calculte_balance(
                dealership.balance, supplier_inventory.price
            )

            self.dealer_inventory_service.set_quantity(
                dealer_request.count,
                dealer_inventory.current_stock,
                inventory_id=dealer_inventory.id,
            )
            self.dealership_service.update(
                id=dealership.id, instance=dealership, data={"balance": new_balance}
            )
            self.dealer_request_serice.update(
                id=dealer_request.id,
                instance=dealer_request,
                data=dict(
                    status=TransactionStatusEnum.COMPLETED,
                    total_price=supplier_inventory.price,
                ),
            )

        except NegativeBalanceException:
            self.dealer_request_serice.update(
                id=dealer_request.id,
                instance=dealer_request,
                data=dict(
                    status=TransactionStatusEnum.COMPLETED,
                    error_description="Nety denyag",
                ),
            )
        except Exception as e:
            raise APIException(
                detail=f"Error during processing data. Detail: {e}",
            )

    def __calculte_balance(self, dealership_balance: Decimal, request_price: Decimal):
        if dealership_balance - request_price < 0:
            raise NegativeBalanceException
