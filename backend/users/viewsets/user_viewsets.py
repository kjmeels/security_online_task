from typing import Any

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from requests import Request
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.permissions import IsCustomerOnly, IsStaffOnly
from ..constants import RoleChoices
from ..serializers.user_serializers import (
    CreateUserSerializer,
    UserSerializer,
    UserEmployeeRetrieveSerializer,
    UserCustomerRetrieveSerializer,
)


@extend_schema(tags=["User"])
class UserViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """Вьюсет пользователя."""

    def get_serializer_class(self) -> type[BaseSerializer] | None:
        if self.action == "about_me":
            if self.request.user.role == RoleChoices.STAFF:
                return UserEmployeeRetrieveSerializer
            else:
                return UserCustomerRetrieveSerializer
        if self.action == "create":
            return CreateUserSerializer
        if self.action == "list":
            return UserSerializer

    def get_queryset(self) -> QuerySet:
        if self.action == "create":
            return User.objects.all()
        if self.action == "about_me":
            if self.request.user.role == RoleChoices.STAFF:
                return User.objects.filter(id=self.request.user.id).prefetch_related("employee_tasks")
            else:
                return User.objects.filter(id=self.request.user.id).prefetch_related("customer_tasks")
        if self.action == "list":
            return User.objects.filter(role=RoleChoices.STAFF)

    def get_permissions(self):
        if self.action == "create":
            return [IsStaffOnly()]
        if self.action == "list":
            return [IsCustomerOnly()]
        return [IsAuthenticated()]

    @action(detail=False, methods=["GET"])
    def about_me(self, request: Request, *args: list[Any], **kwargs: dict[Any, Any]) -> Response:
        serializer = self.get_serializer(self.get_queryset().first())
        return Response(serializer.data)
