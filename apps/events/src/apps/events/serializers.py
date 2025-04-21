from django.utils import timezone
from rest_framework import serializers

from apps.events.models import Event


class EventSerializer(serializers.ModelSerializer):
    """Сериализатор модели Event"""

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "event_date",
            "available_tickets",
            "ticket_price",
            "is_deleted",
        ]

    def validate_event_date(self, value):
        """Проверка, что дата мероприятия не в прошлом."""
        if value < timezone.now():
            raise serializers.ValidationError(
                "Дата мероприятия не может быть в прошлом!"
            )
        return value

    def validate(self, data):
        """Проверка корректности цены и количества билетов."""
        if (
            data.get("available_tickets") is not None
            and data.get("available_tickets") < 0
        ):
            raise serializers.ValidationError(
                "Количество билетов не может быть отрицательным!"
            )

        if data.get("ticket_price") is not None and data.get("ticket_price") < 0:
            raise serializers.ValidationError("Стоимость билетов не может быть ниже 0!")
