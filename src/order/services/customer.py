from typing import Sequence
from uuid import uuid4

from core.services import BaseService
from order.models import CustomerProfile


class CustomerService(BaseService):
    model = CustomerProfile

    def create_profile(self, user_id: uuid4) -> CustomerProfile:
        return CustomerProfile.objects.create(
            user_id=user_id,
        )

    def get_all(self) -> Sequence:
        return CustomerProfile.objects.select_related("user").all()
