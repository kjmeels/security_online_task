from typing import Any

from rest_framework import serializers

from .constants import StatusChoices
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор задач."""

    class Meta:
        model = Task
        fields = (
            "id",
            "status",
            "customer",
            "task_detail",
        )


class TaskDetailSerializer(serializers.ModelSerializer):
    """Сериализатор деталки задач."""

    class Meta:
        model = Task
        fields = (
            "id",
            "status",
            "customer",
            "employee",
            "created_at",
            "updated_at",
            "ended_at",
            "report",
            "task_detail",
        )


class CreateTaskSerializer(serializers.ModelSerializer):
    """Сериализатор на создание задачи."""
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = (
            "customer",
            "task_detail",
        )


class UpdateTaskSerializer(serializers.ModelSerializer):
    """Сериализатор на обновление задачи."""

    class Meta:
        model = Task
        fields = (
            "status",
            "task_detail",
            "report",
        )

    def validate(self, attrs: dict[Any, Any]) -> dict[Any, Any]:
        status = attrs.get("status")
        report = attrs.get("report")
        if status == StatusChoices.COMPLETED and not report:
            raise serializers.ValidationError("Report cannot be empty.")
        return attrs
