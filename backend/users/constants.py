from django.db.models import TextChoices


class RoleChoices(TextChoices):
    STAFF = "staff", "сотрудник"
    CUSTOMER = "customer", "заказчик"
