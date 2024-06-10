from django.db import models

from .constants import StatusChoices


class Task(models.Model):
    status = models.CharField(
        verbose_name="Статус",
        max_length=50,
        null=True,
        blank=True,
        choices=StatusChoices.choices,
    )
    customer = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        verbose_name="Заказчик",
        related_name="customer_tasks",
        null=True,
    )
    employee = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        verbose_name="Сотрудник",
        related_name="employee_tasks",
        null=True,
    )
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    ended_at = models.DateTimeField(verbose_name="Дата закрытия", null=True, blank=True)
    report = models.TextField(verbose_name="Отчет", default="", blank=True)
    task_detail = models.TextField(verbose_name="Детали задачи", default="")

    class Meta:
        verbose_name: str = "Задача"
        verbose_name_plural: str = "Задачи"

    def __str__(self) -> str:
        return f"Задача - {self.pk}. Статус - {self.status}"
