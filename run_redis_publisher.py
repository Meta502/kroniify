import redis, json

conn = redis.Redis(
    port=6380
)

expTime = 1 #In Second
conn.set('3cacf96b-750e-4386-ab05-4d7ca84a98f4', "")
conn.set('valKey:3cacf96b-750e-4386-ab05-4d7ca84a98f4', 'EX', expTime)
print("Publisher : success set event ...")
