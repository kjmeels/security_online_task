from rest_framework import serializers

from ..models import User


class AuthUserSerializer(serializers.ModelSerializer):
    """Сериализатор авторизации пользователя."""

    class Meta:
        model = User
        fields = (
            "phone",
        )
