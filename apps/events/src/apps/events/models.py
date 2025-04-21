from django.core.validators import MinValueValidator
from django.db import models


class EventManager(models.Manager):
    """Менеджер для модели Event, скрывающий удалённые записи"""

    def get_queryset(self):
        """Возвращает записи, исключая удаленные"""
        return super().get_queryset().filter(is_deleted=False)

    def with_deleted(self):
        """Возвращает записи, включая удаленные"""
        return super().get_queryset()

    def only_deleted(self):
        """Возвращает удаленные записи"""
        return super().get_queryset().filter(is_deleted=True)


class Event(models.Model):
    """Модель мероприятия"""

    title = models.CharField(verbose_name="Название мероприятия", max_length=200)
    description = models.TextField(
        verbose_name="Описание мероприятия", blank=True, null=True
    )
    event_date = models.DateTimeField(verbose_name="Дата и время проведения")
    available_tickets = models.IntegerField(
        verbose_name="Количество билетов", default=0, validators=[MinValueValidator(0)]
    )
    ticket_price = models.DecimalField(
        verbose_name="Цена билета",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.10)],
    )

    is_deleted = models.BooleanField(default=False, verbose_name="Мероприятие удалено")

    object = EventManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = ("Мероприятие",)
        verbose_name_plural = "Мероприятия"
        ordering = ["-event_date", "title"]

        indexes = [
            models.Index(fields=["event_date"]),
            models.Index(fields=["is_deleted"])
        ]

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        """Переопределяем метод delete для реализации soft-delete"""
        # Если передан параметр hard_delete=True, то удаляем запись физически
        hard_delete = kwargs.pop('hard_delete', False)
        if hard_delete:
            return super().delete(*args, **kwargs)

        # Иначе помечаем запись как удалённую
        self.is_deleted = True
        self.save()

    def restore(self):
        """Метод для восстановления записи"""
        if self.is_deleted:
            self.is_deleted = False
            self.save()
            return True
        return False
