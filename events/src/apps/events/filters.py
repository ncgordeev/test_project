from django_filters import rest_framework as filters

from apps.events.models import Event


class EventFilter(filters.FilterSet):
    """Фильтр мероприятий по датам."""
    date_from = filters.DateTimeFilter(field_name="event_date", lookup_expr="gte")
    date_to = filters.DateTimeFilter(field_name="event_date", lookup_expr="lte")

    class Meta:
        model = Event
        fields = ["date_from", "date_to"]
