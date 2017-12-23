import json
from functools import wraps


class RedisCache(object):

    def __init__(self, redis_client):
        self._redis = redis_client

    def cache(self, timeout=0):
        def deco(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if timeout == 0:
                    return func(*args, **kwargs)
                key = func.__name__
                value = self._redis.get(key)
                if not value:
                    value = func(*args, **kwargs)
                    self._redis.setex(key, timeout, json.dumps(value))
                    return value
                else:
                    return json.loads(value.decode())
            return wrapper
        return deco
