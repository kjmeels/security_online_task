from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@register(User)
class UserAdmin(UserAdmin):
    list_display = ("phone", "role", "username")
    fieldsets = (
        (None, {"fields": ("username", "password", "phone")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions", "role")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
