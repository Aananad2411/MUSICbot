import redis
import json
from app.config import REDIS_URI, REDIS_PASSWORD

r = redis.Redis.from_url(f"redis://:{REDIS_PASSWORD}@{REDIS_URI}", decode_responses=True)

def add_to_queue(chat_id, track):
    key = f"queue:{chat_id}"
    r.rpush(key, json.dumps(track))

def get_next_track(chat_id):
    key = f"queue:{chat_id}"
    track = r.lpop(key)
    return json.loads(track) if track else None

def get_queue(chat_id):
    key = f"queue:{chat_id}"
    return [json.loads(i) for i in r.lrange(key, 0, -1)]

def clear_queue(chat_id):
    r.delete(f"queue:{chat_id}")
