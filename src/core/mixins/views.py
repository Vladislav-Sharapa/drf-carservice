from uuid import UUID

from rest_framework.request import Request
from rest_framework.response import Response, Serializer

from core.services import BaseService


class UpdateModelMixin:
    service: BaseService = None
    serializer_class: Serializer = None

    def update(self, request: Request, pk: UUID):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.service.update(id=pk, data=serializer.validated_data)
        return Response({"msg": "Record was updated", "detail": serializer.data})
