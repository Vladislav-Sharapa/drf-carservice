from datetime import date, timedelta
from decimal import Decimal

import factory
from factory import faker
import random
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from core.enums import TransactionStatusEnum
from .models import (
    DealerShip,
    DealerShipInventory,
    DealerShipPromotion,
    DealerShipRequest,
)


class DealerShipFactory(DjangoModelFactory):
    class Meta:
        model = DealerShip

    name = factory.Faker("company")

    balance = factory.Faker(
        "pydecimal",
        left_digits=6,
        right_digits=2,
        positive=True,
        min_value=5000,
        max_value=100000,
    )

    address = factory.Faker("address", locale="ru_RU")
    tik_tok_url = factory.Faker("url")
    instagram_url = factory.Faker("url")
    phone_number = factory.Faker("phone_number", locale="ru_RU")


class DealerShipRequestFactory(DjangoModelFactory):
    class Meta:
        model = DealerShipRequest

    dealership = factory.SubFactory("dealer.factories.DealerShipFactory")
    car = factory.SubFactory("supplier.factories.CarModelFactory")
    status = FuzzyChoice(TransactionStatusEnum.values)
    quantity = factory.Faker("random_int", min=1, max=100)
    status_detail = factory.Maybe(
        "decider",
        yes_declaration=factory.Faker("text", max_nb_chars=200),
        no_declaration=None,
    )


class DealerShipInventoryFactory(DjangoModelFactory):
    class Meta:
        model = DealerShipInventory
        django_get_or_create = ("car", "dealership")

    dealership = factory.SubFactory("dealer.factories.DealerShipFactory")
    car = factory.SubFactory("supplier.factories.CarModelFactory")
    current_stock = factory.Faker("pyint", min_value=10, max_value=50)
    min_required_stock = factory.Faker("pyint", min_value=1, max_value=3)
    price = factory.LazyFunction(lambda: Decimal(faker.random_int(1000, 100000)) / 100)


class DealerShipPromotionFactory(DjangoModelFactory):
    class Meta:
        model = DealerShipPromotion
        django_get_or_create = ("name", "dealership")

    dealership = factory.SubFactory("dealer.factories.DealerShipFactory")
    name = factory.Faker("text", max_nb_chars=15)
    start_date = factory.LazyFunction(lambda: date.today())
    end_date = factory.LazyAttribute(
        lambda obj: obj.start_date + timedelta(days=random.randint(7, 90))
    )
    discount_percent = factory.LazyFunction(
        lambda: Decimal(random.randint(0, 100)) / 100
    )
