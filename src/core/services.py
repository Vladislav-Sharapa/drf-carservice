from typing import Any, Dict, Optional, Sequence
from uuid import uuid4

from core.models import BaseModel, CarModel
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound


class BaseService:
    model: Optional[BaseModel] = None

    def get_all(self) -> Sequence:
        return self.model.objects.all()

    def get_by_id(self, id: uuid4):
        try:
            request = self.model.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise NotFound(
                detail=f"Object {self.model.__name__} with id {id} was not found"
            )
        return request

    def update(
        self, id: uuid4, data: Dict[str, Any], instance: BaseModel = None
    ) -> BaseModel:
        if not instance or not isinstance(instance, self.model):
            instance = self.get_by_id(id)
        for field, value in data.items():
            if hasattr(instance, field):
                setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, id: uuid4) -> None:
        instance = self.get_by_id(id)
        instance.delete()


class CarService(BaseService):
    model = CarModel
