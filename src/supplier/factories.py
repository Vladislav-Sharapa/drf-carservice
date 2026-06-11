import factory
from factory.django import DjangoModelFactory
from .models import CarModel, Supplier


class CarModelFactory(DjangoModelFactory):
    """
    Factory to create inst of car model with random data"""

    class Meta:
        model = CarModel

    brand = factory.Faker("company")
    name = factory.Sequence(lambda n: f"car_model_{n}")
    year = factory.Faker("year")
    horsepower = factory.Faker("random_int", min=50, max=800)

    fuel_type = factory.Faker("random_element", elements=CarModel.FuelType.values)
    body_type = factory.Faker("random_element", elements=CarModel.BodyType.values)


class SupplierFactory(DjangoModelFactory):
    class Meta:
        model = Supplier
