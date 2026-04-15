from django.db.models import (
    CharField,
    DecimalField,
    OneToOneField,
    CASCADE,
    ForeignKey,
    PROTECT,
)
from django.contrib.auth.models import User

from core.enums import TransactionStatusEnum
from core.models import BaseModel, CarModel
from dealer.models import DealerShip, DealerShipPromotion


class CustomerProfile(BaseModel):
    user = OneToOneField(User, on_delete=CASCADE)
    balance = DecimalField(max_digits=10, decimal_places=2, default=5000)


class Order(BaseModel):
    dealership = ForeignKey(DealerShip, on_delete=PROTECT)
    car = ForeignKey(CarModel, on_delete=PROTECT)
    customer = ForeignKey(CustomerProfile, on_delete=PROTECT)
    status = CharField(choices=TransactionStatusEnum.choices)
    promotion = ForeignKey(DealerShipPromotion, null=True, on_delete=PROTECT)
    init_price = DecimalField(max_digits=10, decimal_places=2)
    total_price = DecimalField(max_digits=10, decimal_places=2)
