from django.contrib.auth.models import User
from django.db.models.fields import uuid
from django.utils import timezone
from pyawscron import AWSCron

from scheduler.models import Schedule

class EditScheduleService:
    @classmethod
    def run(cls, id: uuid.UUID, data: dict):
        update_data = {
            key: value for key, value in data.items() if value is not None
        }

        schedule_queryset = Schedule.objects.filter(id=id)
        schedule_queryset.update(
            **update_data,
        )

        schedule = schedule_queryset.first()
        next_occurrences = AWSCron.get_next_n_schedule(5, timezone.now(), schedule.cron_expression)

        return {
            "id": schedule.id,
            "payload": schedule.payload,
            "cron_expression": schedule.cron_expression,
            "next_occurrences": next_occurrences,
        }

