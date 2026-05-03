from uuid import UUID

from core.enums import TransactionStatusEnum
from core.services import BaseService
from order.models import Order


class OrderService(BaseService):
    model = Order

    def create(self, car_id: UUID, customer_id: UUID):
        return Order.objects.create(
            car=car_id, customer_id=customer_id, status=TransactionStatusEnum.PENDING
        )
