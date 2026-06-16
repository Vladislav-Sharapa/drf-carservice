from django.db.models import (
    F,
    Q,
    CharField,
    CheckConstraint,
    PositiveSmallIntegerField,
    EmailField,
    TextChoices,
    UniqueConstraint,
    ForeignKey,
    CASCADE,
    DecimalField,
    DateField,
)
from datetime import datetime

from core.mixins.models import DiscountMixin
from core.models import BaseModel


class CarModel(BaseModel):
    class FuelType(TextChoices):
        DIESEL = "DIESEL"
        PETROL = "PETROL"
        GAS = "GAS"

    class BodyType(TextChoices):
        SEDAN = "SEDAN"
        COUPE = "COUPE"
        HATCHBACK = "HATCHBACK"
        ESTATE = "ESTATE"
        CROSSOVER = "CROSSOVER"
        PICKUP = "PICKUP"
        MINIVAN = "MINIVAN"
        CABRIOLET = "CABRIOLET"

    brand = CharField(max_length=45)
    name = CharField(max_length=45, unique=True)
    year = PositiveSmallIntegerField()
    horsepower = PositiveSmallIntegerField()
    fuel_type = CharField(
        max_length=15, choices=FuelType.choices, default=FuelType.PETROL
    )
    body_type = CharField(
        max_length=15, choices=BodyType.choices, default=BodyType.SEDAN
    )

    class Meta:
        app_label = "supplier"


class Supplier(BaseModel):
    name = CharField(max_length=50, unique=True)
    founded_year = PositiveSmallIntegerField()
    contact_email = EmailField()
    phone = CharField(max_length=20)
    address = address = CharField(max_length=50)


class SupplierInventory(BaseModel):
    price = DecimalField(max_digits=10, decimal_places=2)
    supplier = ForeignKey("supplier.Supplier", on_delete=CASCADE)
    car = ForeignKey(CarModel, on_delete=CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["car", "supplier"], name="unique_car_supplier"),
        ]


class SupplierPromotion(BaseModel, DiscountMixin):
    name = CharField(max_length=50)
    supplier = ForeignKey("supplier.Supplier", on_delete=CASCADE)
    start_date = DateField(blank=False, default=datetime.today)
    end_date = DateField(blank=False)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["name", "supplier"], name="unique_name_supplier"),
            CheckConstraint(
                condition=Q(end_date__gt=F("start_date")),
                name="end_date_after_start_date_supplier",
            ),
        ]


class SupplierLoyaltyDiscount(BaseModel, DiscountMixin):
    supplier = ForeignKey("supplier.Supplier", on_delete=CASCADE)
    dealership = ForeignKey(
        "dealer.DealerShip", on_delete=CASCADE, related_name="loyalty_discount"
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["dealership", "supplier"], name="unique_dealership_supplier"
            ),
        ]
