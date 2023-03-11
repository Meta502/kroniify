from scheduler.views.schedule import ScheduleView
from django.urls import path

urlpatterns = [
    path("", ScheduleView.as_view(), name="schedule-view")
]
