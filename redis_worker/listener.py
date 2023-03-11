from pyawscron import AWSCron
from django.utils import timezone

import redis
import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from scheduler.models import Schedule

def event_handler(msg): # pragma: no cover
    try:
        key = msg["data"].decode("utf-8")
        if "valKey" in key:
            key = key.replace("valKey:", "")
            # Process message redis subscriber
            process_message(key)
    except Exception as exp:
        pass

def process_message(key):
    print(f"Event Received: {key}")
    schedule = Schedule.objects.filter(id=key).first()
    next_schedules = AWSCron.get_next_n_schedule(2, timezone.now() + timezone.timedelta(seconds=1), schedule.cron_expression)

    now = timezone.now()
    delta = next_schedules[0] - now

    if int(delta.total_seconds()) == 0:
        delta = next_schedules[1] - now

    conn.set(f'valKey:{schedule.id}', 'EX', int(delta.total_seconds()))
    requests.post(
        schedule.target_url,
        data=json.dumps(schedule.payload),
        headers={
            "Content-Type": "application/json",
        }
    )

# Creating Redis and pubsub Connection
conn = redis.Redis(
    port=6380
)
pubsub = conn.pubsub()

# Set Config redis key expire listener
conn.config_set('notify-keyspace-events', 'Ex')
pubsub.psubscribe(**{"__keyevent@0__:expired": event_handler})
pubsub.run_in_thread(sleep_time=0.01)

print("Running : worker redis subscriber ...")
