import json
import redis
from functools import wraps

from fivestar.settings.common import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_DB, REDIS_EXPIRES_TIME_IN_SECONDS


class CacheManager:
    """
    Class responsible for cache management - use redis as cache
    storing db
    """

    def __init__(self):
        self.__cache_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), db=int(REDIS_DB),
                                          password=REDIS_PASSWORD)

    def get(self, name: str) -> dict or None:
        """
        Method responsible for getting value based on given name
        :param name: key name
        :return: None or cached value
        """
        cached_value = self.__cache_client.get(f'{name}')
        if cached_value:
            return json.loads(cached_value)
        return None

    def set(self, name: str, serializable_value=None, expires=REDIS_EXPIRES_TIME_IN_SECONDS) -> bool:
        """
        Method responsible for setting value based on given name
        :param name: key nameTy w og
        :param serializable_value: serializable value
        :param expires: time in seconds to expire key
        :return: bool
        """
        value = json.dumps(serializable_value)
        try:
            self.__cache_client.set(name=f'{name}', value=value, ex=expires)
        except Exception:
            return False
        return True


def cached(func):
    """
    Decorator responsible for caching serializable values under key
    created based on func/method args and kwargs
    :param func: function
    :return: cached value
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_manager = CacheManager()
        key_parts = [func.__module__, args[0].__class__.__name__, func.__name__] + list(
            ', '.join('%s' % x for x in args[1:])) + list(', '.join('%s=%r' % x for x in kwargs.items()))
        key = '-'.join(key_parts)
        try:
            result = cache_manager.get(key)
        except Exception as ex:
            print(ex)
            result = None
        if result is None:
            value = func(*args, **kwargs)
            cache_manager.set(key, value, expires=REDIS_EXPIRES_TIME_IN_SECONDS)
        else:
            value = result
        return value

    return wrapper
