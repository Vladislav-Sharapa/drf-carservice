from typing import Optional
from uuid import uuid4

from core.models import BaseModel, CarModel
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound


class BaseService:
    model: Optional[BaseModel] = None

    def get_by_id(self, id: uuid4):
        try:
            request = self.model.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise NotFound(
                detail=f"Object {self.model.__name__} with id {id} was not found"
            )
        return request


class CarService(BaseService):
    model = CarModel
