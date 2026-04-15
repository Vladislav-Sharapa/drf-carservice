from django.db.models import (
    DateTimeField,
    Model,
    CharField,
    PositiveSmallIntegerField,
    TextChoices,
)


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class CarModel(BaseModel):
    class FuelType(TextChoices):
        DIESEL = "diesel"
        PETROL = "petrol"
        GAS = "gas"

    class BodyType(TextChoices):
        SEDAN = "sedan"
        COUPE = "coupe"
        HATCHBACK = "hatchback"
        ESTATE = "estate"
        CROSSOVER = "crossover"
        PICKUP = "pickup"
        MINIVAN = "minivan"
        CABRIOLET = "cabriolet"

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
