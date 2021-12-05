from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response

from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegistrationSerializer,
    ForgotPasswordSerializer,
    UserSerializer,
)


class RegistrationViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


class LoginViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


class ChangePasswordViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class ForgotPasswordViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer


class UserViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data)
