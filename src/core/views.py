from typing import Sequence, Type, override

from rest_framework.viewsets import GenericViewSet
from rest_framework.serializers import Serializer


class BaseGenericViewSet(GenericViewSet):
    serializer_map: dict[Type[Serializer], Sequence[str]] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.serializer_map:
            for serializer, actions in self.serializer_map.items():
                if not isinstance(actions, (list, tuple, set)):
                    raise TypeError(
                        f"Value for {serializer.__name__} must be list, tuple or set of actions"
                    )

    @override
    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if not self.serializer_map:
            return serializer_class
        for serializer, actions in self.serializer_map.items():
            if self.action in actions:
                serializer_class = serializer
        return serializer_class
