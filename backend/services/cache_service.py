class CacheService:

    CACHE = {}


    @staticmethod
    def set(key, value):

        CacheService.CACHE[key] = value


    @staticmethod
    def get(key):

        return CacheService.CACHE.get(key)