from scheduler.views.create_schedule import CreateScheduleView
from django.urls import path

from scheduler.views.edit_schedule import EditScheduleView

urlpatterns = [
    path("", CreateScheduleView.as_view(), name="create-schedule"),
    path("<uuid:schedule_id>", EditScheduleView.as_view(), name="edit-schedule")
]
