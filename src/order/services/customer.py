from typing import Sequence
from uuid import UUID
from rest_framework.exceptions import NotFound

from core.services import BaseService
from order.models import CustomerProfile


class CustomerService(BaseService):
    model = CustomerProfile

    def create_profile(self, user_id: UUID) -> CustomerProfile:
        return CustomerProfile.objects.create(
            user_id=user_id,
        )

    def get_all(self) -> Sequence:
        return CustomerProfile.objects.select_related("user").all()

    def get_by_user_id(self, user_id):
        customer = CustomerProfile.objects.get(user_id=user_id)
        if not customer:
            raise NotFound(
                detail=f"There is no customer profile for user with id={user_id}"
            )
        return customer
