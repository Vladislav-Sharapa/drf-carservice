from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User

from authentication.serializers import UserRegistrationSerializer, UserSerializer


class UserService:
    def create_user(self, request: Request) -> Response:
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_all(self):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
