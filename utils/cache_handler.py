import json
import pickle
from pathlib import Path
from typing import List, Dict

from cache import redis_client


def read_from_redis(key: str) -> Dict:
    cached = redis_client.get(key)
    cached_data = pickle.loads(cached)
    return cached_data


def read_from_file(key: str) -> Dict:
    if Path(f"./data/persistence/weather_info_{key}.json").exists():
        with open(f"./data/persistence/weather_info_{key}.json", "r") as f:
            cached_data = json.load(f)
        return cached_data
    else:
        return {}


def save_to_redis(key: str, value: Dict, expiration=3600) -> bool:
    data_bytes = pickle.dumps(value)
    redis_client.set(key, data_bytes, ex=expiration)
    return True


def cache_data(responses: List) -> None:
    for response in responses:
        save_to_redis(key=response["code"], value=response)

    return True


def persist_data(responses: List) -> None:
    for response in responses:
        with open(f"./data/persistence/weather_info_{response['code']}.json", "w+") as output_file:
            json.dump(response, output_file, indent=2)

    return True


def read_cache(airports):
    cache = []
    try:
        for airport in airports:
            read_from_redis(airport)
        cache.append(cached_data)
    except:
        for airport in airports:
            cached_data = read_from_file(airport)
            cache.append(cached_data)
    return cache
