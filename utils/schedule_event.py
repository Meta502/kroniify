from django.db.models.fields import uuid
from django.utils import timezone
from pyawscron import AWSCron
from engines.redis import redis_client

def schedule_event(id: uuid.UUID, cron_expression: str):
    redis_client.delete(f"valKey:{id}")
    next_occurrences = AWSCron.get_next_n_schedule(2, timezone.now(), cron_expression)
    
    now = timezone.now()
    delta = next_occurrences[0] - now

    if int(delta.total_seconds()) == 0:
        delta = next_occurrences[1] - now

    redis_client.set(f"valKey:{id}", "EX", int(delta.total_seconds()))
