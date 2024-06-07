from rest_framework.permissions import IsAuthenticated

from .constants import RoleChoices


class IsStaffOnly(IsAuthenticated):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == RoleChoices.STAFF


class IsCustomerOnly(IsAuthenticated):

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == RoleChoices.CUSTOMER
