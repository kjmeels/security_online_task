from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from requests import Request
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User
from ..serializers.auth_serializers import AuthUserSerializer


@extend_schema(tags=["Authorization"])
class AuthViewSet(GenericViewSet):
    """Вьюсет авторизации пользователя."""

    def get_serializer_class(self) -> type[BaseSerializer] | None:
        return AuthUserSerializer

    @action(detail=False, methods=["POST"])
    def get_tokens(self, request: Request, *args, **kwargs) -> Response:
        """Эндпоинт получения JWT-токенов."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = str(serializer.validated_data["phone"])
        user = get_object_or_404(User, phone=phone_number)
        refresh = RefreshToken.for_user(user)
        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)},
            status=status.HTTP_201_CREATED,
        )
