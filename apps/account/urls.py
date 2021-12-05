from django.urls import path, include

from rest_framework import routers
from .views import (
    LoginViewSet,
    RegistrationViewSet,
    ChangePasswordViewSet,
    ForgotPasswordViewSet,
    UserViewSet
)


app_name = "account"

router = routers.DefaultRouter()
router.register(r"register", RegistrationViewSet, basename="register")
router.register(r"login", LoginViewSet, basename="login")
router.register(r"change_password", ChangePasswordViewSet, basename="change_password")
router.register(r"forgot_password", ForgotPasswordViewSet, basename="forgot_password")
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
