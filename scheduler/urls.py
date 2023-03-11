from scheduler.views.list_create_schedule import ListCreateScheduleView
from django.urls import path

from scheduler.views.edit_delete_schedule import EditDeleteScheduleView

urlpatterns = [
    path("", ListCreateScheduleView.as_view(), name="create-schedule"),
    path("<uuid:schedule_id>", EditDeleteScheduleView.as_view(), name="edit-schedule")
]
