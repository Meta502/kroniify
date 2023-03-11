import redis

conn = redis.Redis(
    port=6380
)

redis_client = conn
