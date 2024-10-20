import os

from redis import Redis

from flask_caching import Cache


cache = Cache()

redis_client = Redis(host=os.getenv("CACHE_REDIS_HOST"), port=os.getenv("CACHE_REDIS_PORT"), db=os.getenv("CACHE_REDIS_DB"))
