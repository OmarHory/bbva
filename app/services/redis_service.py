import json
import redis
from typing import Dict, Any
from app.config.settings import settings

# Create a Redis connection
redis_conn = redis.from_url(
    settings.redis.url, 
    password=settings.redis.password if settings.redis.password else None,
    db=settings.redis.db
)

def get_user_state_key(user_id: str) -> str:
    """Generate a Redis key for user state"""
    return f"{settings.redis.prefix}state:{user_id}"

def save_user_state(user_id: str, state: Dict[str, Any]) -> bool:
    """Save user state to Redis"""
    key = get_user_state_key(user_id)
    try:
        redis_conn.set(key, json.dumps(state))
        return True
    except Exception as e:
        print(f"Error saving user state: {e}")
        return False

def load_user_state(user_id: str) -> Dict[str, Any]:
    """Load user state from Redis"""
    key = get_user_state_key(user_id)
    try:
        state_json = redis_conn.get(key)
        if state_json:
            return json.loads(state_json)
    except Exception as e:
        print(f"Error loading user state: {e}")
    return None 


def delete_user_state_pattern(pattern: str) -> bool:
    """Delete user state from Redis by pattern"""
    try:
        print(f"Deleting user state pattern: {pattern}")
        keys = redis_conn.keys(pattern)
        if keys:
            redis_conn.delete(*keys)
        return True
    except Exception as e:
        print(f"Error deleting user state: {e}")
        return False