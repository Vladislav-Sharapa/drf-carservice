from django.db.models import (
    CharField,
    DecimalField,
    OneToOneField,
    CASCADE,
    ForeignKey,
    PROTECT,
    PositiveSmallIntegerField,
)
from django.contrib.auth.models import User

from core.enums import TransactionStatusEnum
from core.models import BaseModel
from dealer.models import DealerShip, DealerShipPromotion
from supplier.models import CarModel


class CustomerProfile(BaseModel):
    user = OneToOneField(User, on_delete=CASCADE)
    balance = DecimalField(max_digits=10, decimal_places=2, default=5000)


class Order(BaseModel):
    dealership = ForeignKey(DealerShip, on_delete=PROTECT, null=True, blank=True)
    car = ForeignKey(CarModel, on_delete=PROTECT)
    customer = ForeignKey(CustomerProfile, on_delete=PROTECT)
    quantity = PositiveSmallIntegerField(default=1)
    status = CharField(
        choices=TransactionStatusEnum.choices, default=TransactionStatusEnum.PENDING
    )
    promotion = ForeignKey(
        DealerShipPromotion, null=True, on_delete=PROTECT, blank=True
    )
    init_price = DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_price = DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status_detail = CharField(max_length=200, null=True, blank=True)
