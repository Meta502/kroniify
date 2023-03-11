from django.db.models.fields import uuid
from engines.redis import redis_client

def unschedule_event(id: uuid.UUID):
    redis_client.delete(f"valKey:{id}") 
