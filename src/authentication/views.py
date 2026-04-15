from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from .serializers import UserRegistrationSerializer, UserSerializer
from .service import UserService
from drf_spectacular.utils import extend_schema


class UserViewSet(ViewSet):
    user_service = UserService()

    @extend_schema(request=UserRegistrationSerializer)
    def create(self, request):
        response = self.user_service.create_user(request)

        return response

    @extend_schema(request=UserSerializer)
    def list(self, request: Request):
        response = self.user_service.get_all()

        return response
