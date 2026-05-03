from datetime import datetime

from django.db.models import (
    F,
    Q,
    CharField,
    CheckConstraint,
    DateField,
    DecimalField,
    TextField,
    URLField,
    ForeignKey,
    CASCADE,
    PROTECT,
    PositiveSmallIntegerField,
    UniqueConstraint,
)
from django.core.validators import MinValueValidator

from core.enums import TransactionStatusEnum
from core.mixins.models import DiscountMixin
from core.models import BaseModel
from supplier.models import CarModel


class DealerShip(BaseModel):
    name = CharField(max_length=30, unique=True)
    balance = DecimalField(max_digits=10, decimal_places=2, default=10000)
    address = CharField(max_length=50)
    tik_tok_url = URLField(blank=True, null=True, verbose_name="Tik tok")
    instagram_url = URLField(blank=True, null=True, verbose_name="Instagram")
    phone_number = CharField(max_length=15)


class DealerShipInventory(BaseModel):
    dealership = ForeignKey(
        "dealer.DealerShip", on_delete=CASCADE, related_name="inventory"
    )
    car = ForeignKey(CarModel, on_delete=CASCADE)
    current_stock = PositiveSmallIntegerField(default=0)
    min_required_stock = PositiveSmallIntegerField(default=1)
    price = DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["car", "dealership"], name="unique_car_dealerships"
            ),
        ]


class DealerShipPromotion(BaseModel, DiscountMixin):
    name = CharField(max_length=30)
    dealership = ForeignKey(
        "dealer.DealerShip", on_delete=CASCADE, related_name="promotions"
    )
    start_date = DateField(blank=False, default=datetime.today)
    end_date = DateField(blank=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["name", "dealership"], name="unique_name_dealership"
            ),
            CheckConstraint(
                condition=Q(end_date__gt=F("start_date")),
                name="end_date_after_start_date",
            ),
        ]


class DealerShipRequest(BaseModel):
    dealership = ForeignKey(
        "dealer.DealerShip", on_delete=PROTECT, related_name="requests"
    )
    car = ForeignKey(CarModel, on_delete=PROTECT)
    status = CharField(
        choices=TransactionStatusEnum.choices, default=TransactionStatusEnum.PENDING
    )
    quantity = PositiveSmallIntegerField(default=1)
    status_detail = TextField(max_length=200, blank=True, null=True)
    init_price = DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    supplier = ForeignKey("supplier.Supplier", on_delete=PROTECT, null=True)
