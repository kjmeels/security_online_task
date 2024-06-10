from django.db.models import TextChoices


class StatusChoices(TextChoices):
    AWAITS = "awaits", "ожидает"
    IN_PROGRESS = "in_progress", "в процессе"
    COMPLETED = "completed", "выполнена"
