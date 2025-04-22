from django_filters import rest_framework as filters

from apps.events.models import Event


class EventFilter(filters.FilterSet):
    """Фильтр мероприятий по датам."""

    # Фильтр по конкретной дате
    date = filters.DateFilter(field_name="event_date", lookup_expr="date")

    # Фильтр по диапазону дат
    date_from = filters.DateTimeFilter(field_name="event_date", lookup_expr="gte")
    date_to = filters.DateTimeFilter(field_name="event_date", lookup_expr="lte")

    class Meta:
        model = Event
        fields = ["date", "date_from", "date_to"]
