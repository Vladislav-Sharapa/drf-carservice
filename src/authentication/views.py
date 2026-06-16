from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from order.services.customer import CustomerService
from .serializers import UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


class UserCreateViewSet(ViewSet):
    serializer_class = UserRegistrationSerializer
    service = CustomerService()

    @transaction.atomic
    def create(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.service.create_profile(user_id=user.id)
            return Response(
                {"message": "User registered successfully", "user_id": user.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
