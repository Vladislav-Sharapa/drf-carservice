from typing import Any, Dict, Optional, Sequence, Union
from uuid import UUID

from core.models import BaseModel
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound


class BaseService:
    model: Optional[BaseModel] = None

    def get_all(self) -> Sequence:
        return self.model.objects.all()

    def get_by_id(self, id: UUID):
        try:
            request = self.model.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise NotFound(
                detail=f"Object {self.model.__name__} with id {id} was not found"
            )
        return request

    def update(self, obj: Union[UUID, BaseModel], data: Dict[str, Any]) -> BaseModel:
        if isinstance(obj, UUID):
            instance = self.get_by_id(obj)
        elif isinstance(obj, self.model):
            instance = obj
        else:
            raise ValueError(
                f"obj must be {self.model.__name__} instance or UUID, got {type(obj)}"
            )

        for field, value in data.items():
            if hasattr(instance, field):
                setattr(instance, field, value)
        instance.save(update_fields=data.keys())
        return instance

    def delete(self, id: UUID) -> None:
        instance = self.get_by_id(id)
        instance.delete()
