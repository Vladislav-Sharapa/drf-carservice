from decimal import Decimal
from typing import Optional
from uuid import UUID

from core.enums import TransactionStatusEnum
from dealer.models import DealerShipRequest
from dealer.services.dealer_reqeust import DealerShipRequestService
from dealer.services.dealership import DealerShipService
from rest_framework.exceptions import APIException, NotFound
from django.db import IntegrityError, transaction

from dealer.services.inventory import DealerShipInventoryService
from supplier.models import SupplierInventory
from supplier.services.car import CarService
from supplier.services.inventory import SupplierInventoryService


class DealerRequestCreateFlow:
    def __init__(self):
        self.dealer_request_service = DealerShipRequestService()
        self.dealership_service = DealerShipService()
        self.car_service = CarService()

    @transaction.atomic
    def execute(self, dealer_id: UUID, car_id: UUID, quantity: int):
        dealership = self.dealership_service.get_by_id(dealer_id)
        car = self.car_service.get_by_id(car_id)

        try:
            response = self.dealer_request_service.deploy_request(
                dealership=dealership, car=car, quantity=quantity
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

    def execute(self, request: DealerShipRequest):
        """Processing a dealer's order to purchase a car from suppliers
        1. We find the best offer from suppliers, based on all dealer promotions and loyalty discounts
        2. If an offer is found, we check whether the dealer has enough funds to purchase the car at that price
        3. If the dealer has enough funds, we update the dealer's balance and the number of cars in stock
        """
        self._set_request_status(request, status=TransactionStatusEnum.PROCESSING)

        inventory = self.supplier_inventory_service.get_cheapest_inventory(
            car_id=request.car_id, quantity=request.quantity
        )
        if not inventory:
            raise NotFound(detail="There is no supplier with desired car")
        new_dealer_balance = self._calculate_dealer_balance(
            dealer_balance=request.dealership.balance,
            total_price=inventory.price_with_discount,
        )
        if new_dealer_balance < 0:
            self._set_request_status(
                request=request,
                status=TransactionStatusEnum.FAILED,
                message="Dealer has insufficient balance",
            )
            return

        try:
            with transaction.atomic():
                self.dealership_service.update(
                    obj=request.dealership_id, data={"balance": new_dealer_balance}
                )
                self.dealer_inventory_service.update_quantity(
                    dealer_id=request.dealership_id,
                    car_id=request.car_id,
                    quantity=request.quantity,
                )
                self._complete_request(request=request, inventory=inventory)
        except IntegrityError:
            self._set_request_status(
                request=request,
                status=TransactionStatusEnum.ERROR,
                message="Error during server processing",
            )

    def _set_request_status(
        self, request: DealerShipRequest, status: str, message: Optional[str] = None
    ):
        self.dealer_request_serice.update(
            obj=request, data=dict(status=status, status_detail=message)
        )

    def _calculate_dealer_balance(self, dealer_balance: Decimal, total_price: Decimal):
        return dealer_balance - total_price

    def _complete_request(
        self, request: DealerShipRequest, inventory: SupplierInventory
    ):
        self.dealer_request_serice.update(
            obj=request,
            data=dict(
                supplier=inventory.supplier,
                status=TransactionStatusEnum.COMPLETED,
                status_detail="Request was processed",
                init_price=inventory.price,
                total_price=inventory.price_with_discount,
            ),
        )
