from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from utils import messages, tools
from .models import User
from .tasks import forgot_password_task, create_team_for_user


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "token"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        create_team_for_user.delay(user.id)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=8)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        user = authenticate(username=email, password=password)

        if user is None:
            raise ValidationError(messages.INCORRECT_PASSWORD_OR_USER)

        if not user.is_active:
            raise ValidationError(messages.NONE_ACTIVE_USER)

        return {"email": user.email, "username": user.username, "token": user.token}

    def create(self, validated_data):
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
        )


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    new_password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    new_password_confirm = serializers.CharField(
        max_length=255, min_length=8, write_only=True
    )
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "old_password",
            "new_password",
            "new_password_confirm",
        )

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password_confirm"):
            raise ValidationError(messages.PASSWORDS_DO_NOT_MATCH)
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    message = serializers.CharField(read_only=True)

    def create(self, validated_data):
        email = self.validated_data["email"]
        new_password = tools.get_random_password()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as error:
            return {"message": str(error)}
        user.set_password(new_password)
        user.save()
        forgot_password_task.delay(self.validated_data["email"], new_password)
        return {"message": messages.FORG0T_PASSWORD_SUCCESS}
