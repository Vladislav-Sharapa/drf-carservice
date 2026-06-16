from decimal import Decimal
from typing import Optional

from core.enums import TransactionStatusEnum
from dealer.models import DealerShipInventory
from dealer.services.dealership import DealerShipService
from dealer.services.inventory import DealerShipInventoryService
from order.models import Order
from order.services.customer import CustomerService
from order.services.order import OrderService
from django.db import IntegrityError, transaction
from rest_framework.exceptions import NotFound


class OrderProcessingFlow:
    def __init__(self):
        self.order_service = OrderService()
        self.customer_service = CustomerService()
        self.inventory_service = DealerShipInventoryService()
        self.dealer_service = DealerShipService()

    def execute(self, order: Order) -> Order:
        """Processing a customer's car purchase order.
        1. We find the best offer from suppliers, taking into account all promotions
        2. If an offer is found, we check whether the customer has enough money to purchase the car
        3. If there is enough money, we calculate the dealer's balance and the number of cars in the dealer's inventory
        4. We update the database for the customer, dealer (balance), and the number of cars in stock (at the dealer)
        5. Mark the order as completed
        """

        self._set_order_status(order, status=TransactionStatusEnum.PROCESSING)

        inventory: DealerShipInventory = (
            self.inventory_service.get_profitable_inventory(
                order.car_id, order.quantity
            )
        )
        if not inventory:
            self._set_order_status(
                order=order,
                status=TransactionStatusEnum.FAILED,
                message="here is no dealership with desired car",
            )
            raise NotFound(detail="There is no dealership with desired car")

        new_customer_balance = self._calculate_customer_balance(
            dealer_price=inventory.price_with_discount,
            customer_balance=order.customer.balance,
        )
        # If user balance will be lower than zero -> end transaction
        if new_customer_balance < 0:
            self._set_order_status(
                order=order,
                status=TransactionStatusEnum.FAILED,
                message="User has insufficient balance",
            )
            return

        new_dealer_balance = self._calculate_dealer_balance(
            dealer_price=inventory.price_with_discount,
            dealer_balance=inventory.dealership.balance,
        )
        new_inventory_car_quantity = self._calculate_inventory_car_quantity(
            current_stock=inventory.current_stock, order_quantity=order.quantity
        )

        try:
            with transaction.atomic():
                self.customer_service.update(
                    order.customer.id, {"balance": new_customer_balance}
                )
                self.dealer_service.update(
                    inventory.dealership_id, {"balance": new_dealer_balance}
                )
                self.inventory_service.update(
                    inventory.id, {"current_stock": new_inventory_car_quantity}
                )

                self._complete_order(order=order, inventory=inventory)

        except IntegrityError:
            self._set_order_status(
                order=order,
                status=TransactionStatusEnum.ERROR,
                message="Error during server processing",
            )
        finally:
            order.refresh_from_db()

        return order

    def _complete_order(self, order: Order, inventory: DealerShipInventory) -> None:
        """Complete order and save changes in DB"""
        self.order_service.update(
            obj=order,
            data=dict(
                dealership=inventory.dealership,
                status=TransactionStatusEnum.COMPLETED,
                status_detail="Order was processed",
                init_price=inventory.price,
                total_price=inventory.price_with_discount,
            ),
        )

    def _set_order_status(
        self, order: Order, status: str, message: Optional[str] = None
    ) -> None:
        """Set status for order"""
        self.order_service.update(
            obj=order, data=dict(status=status, status_detail=message)
        )

    def _calculate_customer_balance(
        self, dealer_price: Decimal, customer_balance: Decimal
    ) -> bool:
        return customer_balance - dealer_price

    def _calculate_dealer_balance(
        self, dealer_price: Decimal, dealer_balance: Decimal
    ) -> Decimal:
        return dealer_balance + dealer_price

    def _calculate_inventory_car_quantity(
        self, current_stock: int, order_quantity: int
    ):
        return current_stock - order_quantity
