from django.urls import path

from apps.events.apps import EventsConfig
from apps.events.views import (
    EventRestoreAPIView,
    EventsCreateAPIView,
    EventsDeleteAPIView,
    EventsDetailAPIView,
    EventsListAPIView,
    EventsUpdateAPIView,
)

app_name = EventsConfig.name

urlpatterns = [
    path("create/", EventsCreateAPIView.as_view(), name="event_create"),
    path("update/<int:pk>", EventsUpdateAPIView.as_view(), name="event_update"),
    path("restore/<int:pk>", EventRestoreAPIView.as_view(), name="event_update"),
    path("delete/<int:pk>", EventsDeleteAPIView.as_view(), name="event_delete"),
    path("<int:pk>", EventsDetailAPIView.as_view(), name="event_detail"),
    path("", EventsListAPIView.as_view(), name="event_list"),
]
