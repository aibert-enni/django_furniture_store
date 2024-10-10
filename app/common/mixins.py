from django.core.cache import cache

class CacheMixin:
    def set_get_cache(self, query, cache_name, cache_time=60):
        data = cache.get(cache_name)
        if data is None:
            data = query
            cache.set(cache_name, data, cache_time)
        return data