from uuid import UUID
from django.utils import timezone
from core.services import BaseService
from supplier.models import (
    SupplierInventory,
    SupplierLoyaltyDiscount,
    SupplierPromotion,
)
from rest_framework.exceptions import NotFound
from django.db.models import (
    F,
    Q,
    DecimalField,
    Case,
    When,
    Value,
    Max,
    OuterRef,
    Subquery,
)
from django.db.models.functions import Coalesce


class SupplierInventoryService(BaseService):
    model = SupplierInventory

    def get_cheapest_inventory(self, car_id: UUID, quantity: int):
        current_date = timezone.now().date()

        active_loyalty_discount = (
            SupplierLoyaltyDiscount.objects.filter(supplier_id=OuterRef("supplier_id"))
            .annotate(loyalty_discount=F("discount_percent"))
            .values("loyalty_discount")
        )

        active_max_supplier_promotion = (
            SupplierPromotion.objects.filter(
                supplier_id=OuterRef("supplier_id"),
                start_date__lte=current_date,
                end_date__gte=current_date,
            )
            .values("supplier_id")
            .annotate(promotion_discount=Max("discount_percent"))
            .values("promotion_discount")
        )

        result = (
            SupplierInventory.objects.filter(
                car_id=car_id,
            )
            .select_related("supplier")
            .annotate(
                loyalty_discount_percent=Coalesce(
                    Subquery(active_loyalty_discount),
                    Value(0.0),
                    output_field=DecimalField(),
                ),
                promotion_discount_percent=Coalesce(
                    Subquery(active_max_supplier_promotion),
                    Value(0.0),
                    output_field=DecimalField(),
                ),
                discount_price=Case(
                    When(
                        Q(promotion_discount_percent__gt=0)
                        & Q(
                            promotion_discount_percent__gt=F("loyalty_discount_percent")
                        ),
                        then=F("promotion_discount_percent") * F("price"),
                    ),
                    default=F("loyalty_discount_percent") * F("price"),
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

    def get(self, supplier_id: UUID, car_id: UUID) -> SupplierInventory:
        instance = SupplierInventory.objects.filter(
            supplier_id=supplier_id, car_id=car_id
        )
        if not instance:
            raise NotFound(
                detail=f"There is no inventory for supplier with id:{supplier_id}"
            )
        return instance
