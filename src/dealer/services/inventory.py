from decimal import Decimal
from uuid import uuid4

from core.models import CarModel
from core.services import BaseService
from dealer.exceptions import (
    DuplicateInventoryException,
    NegativeInventoryCountException,
)
from dealer.models import DealerShip, DealerShipInventory
from rest_framework.exceptions import NotFound


class DealerShipInventoryService(BaseService):
    model = DealerShipInventory

    def get(self, dealer_id: uuid4, car_id: uuid4) -> DealerShipInventory:
        instance = DealerShipInventory.objects.filter(
            dealer_id=dealer_id, car_id=car_id
        )
        if not instance:
            raise NotFound(
                detail=f"There is no inventory for dealership with id:{dealer_id}"
            )
        return instance

    def set_quantity(
        self, request_quantity: int, current_stock: int, inventory_id: uuid4
    ) -> None:
        result_quantity = current_stock + request_quantity
        if result_quantity < 0:
            raise NegativeInventoryCountException

        self.update(id=inventory_id, data=dict(current_stock=result_quantity))

    def create_inventory(
        self,
        car: CarModel,
        dealership: DealerShip,
        quantity: int,
        price: Decimal,
        min_stock: int = 1,
    ) -> DealerShipInventory:
        inventory = DealerShipInventory.objects.filter(car=car, dealership=dealership)
        if inventory.exists():
            raise DuplicateInventoryException

        return DealerShipInventory.objects.create(
            car=car,
            dealearship=dealership,
            current_stock=quantity,
            min_stock=min_stock,
            price=price,
        )
