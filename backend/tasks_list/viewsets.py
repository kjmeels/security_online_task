from typing import Any

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from requests import Request
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from users.constants import RoleChoices
from users.permissions import IsStaffOnly
from .constants import StatusChoices
from .models import Task
from .serializers import TaskSerializer, CreateTaskSerializer, UpdateTaskSerializer, TaskDetailSerializer


@extend_schema(tags=["Tasks"])
class TaskViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet
):
    """Вьюсет задач."""

    def get_serializer_class(self) -> type[BaseSerializer] | None:
        if self.action == "create":
            return CreateTaskSerializer
        if self.action == "list":
            return TaskSerializer
        if self.action == "update":
            return UpdateTaskSerializer
        if self.action == "retrieve":
            return TaskDetailSerializer

    def get_queryset(self) -> QuerySet | None:
        if self.request.user.role == RoleChoices.STAFF:
            if self.action == "add_task":
                return Task.objects.filter(status=StatusChoices.AWAITS, employee__isnull=True)
            if self.action == "list":
                return Task.objects.all()
            if self.action == "update":
                return Task.objects.filter(employee=self.request.user).exclude(status=StatusChoices.COMPLETED)
        else:
            if self.action == "list":
                return Task.objects.filter(customer=self.request.user)
        return None

    def get_permissions(self):
        if self.action == "update":
            return [IsStaffOnly()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["POST"])
    def add_task(self, request: Request, *args: list[Any], **kwargs: dict[Any, Any]) -> Response:
        task = self.get_object()
        task.employee = self.request.user
        task.save()
        return Response(status=status.HTTP_201_CREATED)
