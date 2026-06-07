from uuid import UUID

from core.enums import TransactionStatusEnum
from core.services import BaseService
from order.models import Order
from django.db.models import QuerySet, Sum, Count


class OrderService(BaseService):
    model = Order

    def create(self, car_id: UUID, customer_id: UUID):
        return Order.objects.create(
            car=car_id, customer_id=customer_id, status=TransactionStatusEnum.PENDING
        )

    def get_by_status(self, status: str):
        orders = Order.objects.filter(status=status).all()
        if not orders.exists():
            return []
        return orders

    def get_completed_orders_income(self, orders: QuerySet) -> dict:
        total = orders.filter(status=TransactionStatusEnum.COMPLETED).aggregate(
            total_income=Sum("total_price"), order_count=Count("id")
        )

        return {
            "order_count": total["order_count"],
            "total_income": total["total_income"],
        }
