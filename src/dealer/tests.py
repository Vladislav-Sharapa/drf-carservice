from uuid import uuid4

from django.test import TestCase

from dealer.factories import (
    DealerShipFactory,
    DealerShipInventoryFactory,
    DealerShipPromotionFactory,
    DealerShipRequestFactory,
)
from rest_framework.exceptions import NotFound
from dealer.services.dealership import DealerShipService
from dealer.services.inventory import DealerShipInventoryService
from supplier.factories import CarModelFactory
from django.db.models import QuerySet


class DealershipServiceTestCase(TestCase):
    def setUp(self):
        self.service = DealerShipService()
        self.dealer = DealerShipFactory.create()

    def test_get_request_by_dealer_id(self):
        car = CarModelFactory.create()
        DealerShipRequestFactory.create(dealership=self.dealer, car=car)

        result = self.service.get_requests(self.dealer.id, None)

        self.assertIsInstance(result, QuerySet)
        self.assertEqual(result.count(), 1)

    def test_get_requests_by_dealer_id(self):
        car = CarModelFactory.create()
        DealerShipRequestFactory.create_batch(size=5, dealership=self.dealer, car=car)

        result = self.service.get_requests(self.dealer.id, None)

        self.assertIsInstance(result, QuerySet)
        self.assertEqual(result.count(), 5)

    def test_get_requests_empty_collection(self):
        with self.assertRaises(NotFound):
            self.service.get_requests(self.dealer.id, None)

    def test_get_requests_nonexistent_dealership(self):
        fake_id = uuid4()

        with self.assertRaises(NotFound):
            self.service.get_requests(fake_id, filters={})

    def test_get_requests_with_filters(self):
        cars = [
            CarModelFactory.create(name="Honda"),
            CarModelFactory.create(name="BMW"),
        ]
        for car in cars:
            DealerShipRequestFactory.create(dealership=self.dealer, car=car)
        filters = {"car__name": "Honda"}

        result = self.service.get_requests(self.dealer.id, filters)

        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().car.name, "Honda")


class DealerShipInventoryServiceTestCase(TestCase):
    def setUp(self):
        self.service = DealerShipInventoryService()
        self.car = CarModelFactory.create()

    def test_get_profitable_inventory(self):
        dealers = DealerShipFactory.create_batch(3)
        DealerShipInventoryFactory.create(
            dealership=dealers[0], car=self.car, price=103
        )
        DealerShipInventoryFactory.create(
            dealership=dealers[1], car=self.car, price=1000
        )
        DealerShipInventoryFactory.create(
            dealership=dealers[2], car=self.car, price=10101
        )

        result = self.service.get_profitable_inventory(self.car.id, 1)

        self.assertEqual(result.price, 103)

    def test_get_profitable_inventory_with_promotion(self):
        """Promotion of second dealer is 50%"""
        dealers = DealerShipFactory.create_batch(2)
        DealerShipPromotionFactory.create(dealership=dealers[1], discount_percent=0.50)
        DealerShipInventoryFactory.create(
            dealership=dealers[0], car=self.car, price=130
        )
        DealerShipInventoryFactory.create(
            dealership=dealers[1], car=self.car, price=160
        )

        result = self.service.get_profitable_inventory(self.car.id, 1)

        self.assertEqual(result.dealership, dealers[1])
        self.assertEqual(result.price_with_discount, 80)
