import aioredis
from typing import Iterable
from .config import CacheConfig

_ABSTRACT_METHOD = 'Abstract Method'


class CacheClient:
    def __init__(self, cache_config: CacheConfig):
        self.cache_config = cache_config

    async def has(self, key: str):
        raise NotImplementedError(_ABSTRACT_METHOD)

    async def add(self, key: str, value: dict):
        raise NotImplementedError(_ABSTRACT_METHOD)

    async def get(self, key: str) -> dict:
        raise NotImplementedError(_ABSTRACT_METHOD)


class MockCacheClient(CacheClient):
    def __init__(self, config):
        super(MockCacheClient, self).__init__(config)
        self.objects = {}

    async def add(self, key: str, value: dict):
        self.objects[key] = value
        return value

    async def get(self, key: str) -> dict:
        return self.objects[key]

    async def has(self, key: str):
        return key in self.objects

    async def get_all(self) -> Iterable[dict]:
        return self.objects

    def clear(self):
        self.objects = {}


class RedisClient(CacheClient):
    def __init__(self, cache_config):
        super().__init__(cache_config)

    async def client(self):
        client = None
        try:
            client = await aioredis.create_redis_pool(self.cache_config.host)
            yield client
        except Exception as e:
            print(e)
            raise Exception('Cannot create client')
        finally:
            if client is not None:
                client.close()
                await client.wait_closed()

    async def add(self, key: str, value: dict):
        try:
            async with self.client() as redis:
                return await redis.set(key, value)
        except Exception as e:
            print(e)
            raise Exception('Impossible to add to cache')

    async def get(self, key: str) -> dict:
        try:
            async with self.client() as redis:
                return await redis.get(key, encoding='utf-8')
        except Exception as e:
            print(e)
            raise Exception('Impossible to get from cache')

