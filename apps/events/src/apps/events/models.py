from django.core.validators import MinValueValidator
from django.db import models


class Event(models.Model):
    """Модель мероприятия"""

    title = models.CharField(
        verbose_name="Название мероприятия",
        max_length=200
    )
    description = models.TextField(
        verbose_name="Описание мероприятия",
        blank=True,
        null=True
    )
    event_date = models.DateTimeField(
        verbose_name="Дата и время проведения"
    )
    available_tickets = models.IntegerField(
        verbose_name="Количество билетов",
        default=0,
        validators=[MinValueValidator(0)]
    )
    ticket_price = models.DecimalField(
        verbose_name="Цена билета",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.10)],
    )

    class Meta:
        verbose_name = "Мероприятие",
        verbose_name_plural = "Мероприятия"
        ordering = ["-event_date", "title"]

    def __str__(self):
        return self.title
