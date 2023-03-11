from typing import Any, Dict
from django.contrib.auth.models import User
from django.db.models.fields import uuid
from django.utils import timezone
from pyawscron import AWSCron

from scheduler.models import Schedule

class CreateScheduleService:
    @classmethod
    def run(cls, user: User, payload: Dict[str, Any], cron_expression: str, target_url: str):
        cron_schedule = AWSCron.get_next_n_schedule(5, timezone.now(), cron_expression)

        schedule = Schedule.objects.create(
            user=user,
            payload=payload,
            cron_expression=cron_expression,
            target_url=target_url,
        )

        return {
            "id": schedule.id, 
            "payload": payload,
            "cron_expression": cron_expression,
            "next_occurrences": cron_schedule,
        }

