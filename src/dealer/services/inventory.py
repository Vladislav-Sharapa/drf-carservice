from decimal import Decimal
from uuid import UUID, uuid4

from core.services import BaseService
from dealer.exceptions import (
    DuplicateInventoryException,
    NegativeInventoryCountException,
)
from dealer.models import DealerShip, DealerShipInventory, DealerShipPromotion
from rest_framework.exceptions import NotFound

from supplier.models import CarModel

from django.db.models import F, DecimalField, Case, When, Value, Max, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.utils import timezone


class DealerShipInventoryService(BaseService):
    model = DealerShipInventory

    def get_profitable_inventory(self, car_id: UUID, quantity: int):
        """
        Finds the most profitable dealership inventory for a car considering active promotions.

        Selects the first available inventory (with sufficient stock) applying the dealer's
        maximum active discount and sorting by final discounted price.

        Args:
            car_id: Car ID to search for
            quantity: Minimum required stock quantity

        Returns:
            DealerShipInventory: Cheapest inventory considering discount and availability,
            none if no suitable inventory found
        """
        current_date = timezone.now().date()

        active_max_dealer_promotion = (
            DealerShipPromotion.objects.filter(
                dealership_id=OuterRef("dealership_id"),
                start_date__lte=current_date,
                end_date__gte=current_date,
            )
            .values("dealership_id")
            .annotate(max_discount=Max("discount_percent"))
            .values("max_discount")
        )

        result = (
            DealerShipInventory.objects.filter(
                car_id=car_id, current_stock__gte=quantity
            )
            .select_related("dealership")
            .annotate(
                max_discount=Coalesce(
                    Subquery(active_max_dealer_promotion),
                    Value(0.0),
                    output_field=DecimalField(),
                ),
                discount_price=Case(
                    When(max_discount__gt=0, then=F("price") * F("max_discount")),
                    default=0,
                    output_field=DecimalField(),
                ),
                price_with_discount=Coalesce(
                    (F("price") - F("discount_price")) * quantity,
                    Value("price"),
                    output_field=DecimalField(),
                ),
            )
            .order_by("price_with_discount")
            .first()
        )

        return result

    def list(self):
        return DealerShipInventory.objects.all().prefetch_related("car")

    def get_by_car_id(self, car_id):
        return DealerShipInventory.objects.filter(car_id=car_id)

    def get(self, dealer_id: uuid4, car_id: uuid4) -> DealerShipInventory:
        instance = DealerShipInventory.objects.filter(
            dealer_id=dealer_id, car_id=car_id
        )
        if not instance:
            raise NotFound(
                detail=f"There is no inventory for dealership with id:{dealer_id}"
            )
        return instance

    def update_quantity(self, dealer_id: UUID, car_id: UUID, quantity: int):
        DealerShipInventory.objects.filter(
            dealership_id=dealer_id, car_id=car_id
        ).update(current_stock=F("current_stock") + quantity)

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
