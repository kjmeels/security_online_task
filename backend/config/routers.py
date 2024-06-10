from rest_framework.routers import DefaultRouter

from tasks_list.viewsets import TaskViewSet

from users.viewsets.auth_viewsets import AuthViewSet
from users.viewsets.user_viewsets import UserViewSet

router = DefaultRouter()

router.register("users", UserViewSet, basename="users")
router.register("tasks_list", TaskViewSet, basename="tasks_list")
router.register("auth_user", AuthViewSet, basename="auth_user")
