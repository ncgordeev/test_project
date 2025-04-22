import logging
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.exceptions import ValidationError

from apps.events.filters import EventFilter
from apps.events.models import Event
from apps.events.pagination import EventPagination
from apps.events.permissions import IsAdmin, IsUser
from apps.events.serializers import EventSerializer

logger = logging.getLogger("events")


class EventsCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт для создания мероприятия.
    """

    permission_classes = (IsAdmin,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
            logger.info(
                f"Event {serializer.instance.id} created by {self.request.user}"
            )
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            raise


class EventsDeleteAPIView(generics.DestroyAPIView):
    """
    Эндпоинт для удаления мероприятия.
    """

    permission_classes = (IsAdmin,)
    queryset = Event.objects.all()

    def perform_destroy(self, instance):
        """
        Soft-delete.
        """
        instance.delete(hard_delete=False)
        logger.info(f"Event {instance.id} deleted by {self.request.user}")


class EventsUpdateAPIView(generics.UpdateAPIView):
    """
    Эндпоинт для изменения мероприятия.
    """

    permission_classes = (IsAdmin,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventRestoreAPIView(generics.UpdateAPIView):
    """
    Эндпоинт для восстановления удаленного мероприятия.
    """

    permission_classes = (IsAdmin,)
    queryset = Event.all_objects.filter(is_deleted=True)
    serializer_class = EventSerializer

    def perform_update(self, serializer):
        instance = self.get_object()
        instance.restore()  # Вызывает метод restore модели Event
        logger.info(f"Event {instance.id} restored by {self.request.user}")


class EventsListAPIView(generics.ListAPIView):
    """
    Эндпоинт отображения списка мероприятий.
    """

    permission_classes = (IsUser,)
    serializer_class = EventSerializer
    pagination_class = EventPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = EventFilter
    ordering_fields = ("event_date",)

    def get_queryset(self):
        return Event.objects.filter(
            event_date__gt=timezone.now(), available_tickets__gt=0
        ).order_by("event_date")


class EventsDetailAPIView(generics.RetrieveAPIView):
    """
    Эндпоинт подробного отображения мероприятия.
    """

    permission_classes = (IsUser,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer
