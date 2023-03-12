from django.core.management import os
import redis

conn = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379"))
)

redis_client = conn
