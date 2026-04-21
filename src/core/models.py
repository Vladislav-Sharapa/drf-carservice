from django.db.models import (
    DateTimeField,
    Model,
    CharField,
    PositiveSmallIntegerField,
    TextChoices,
)


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
