from rest_framework import serializers

from tasks_list.serializers import TaskSerializer
from users.constants import RoleChoices
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "role",
            "email",
            "phone",
            "photo",
        )


class UserCustomerRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    customer_tasks = TaskSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "role",
            "email",
            "phone",
            "photo",
            "customer_tasks",
        )


class UserEmployeeRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    employee_tasks = TaskSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "role",
            "email",
            "phone",
            "photo",
            "employee_tasks",
        )


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя."""

    role = serializers.ChoiceField(choices=RoleChoices.choices)

    class Meta:
        model = User
        fields = (
            "username",
            "role",
            "email",
            "phone",
            "photo",
        )
