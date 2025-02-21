import os
from dataclasses import dataclass
from dotenv import load_dotenv

from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from redis.asyncio import Redis

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str

    SMSBOWER_API_URL: str
    SMSBOWER_TOKEN: str

    SEEONLINE_API_URL: str

    ALLOWED_USERS: list[int]

    REDIS_URL: str


def load_config() -> Config:
    return Config(
        BOT_TOKEN=os.getenv("BOT_TOKEN"),
        SMSBOWER_API_URL=os.getenv("SMSBOWER_API_URL"),
        SMSBOWER_TOKEN=os.getenv("SMSBOWER_TOKEN"),
        SEEONLINE_API_URL=os.getenv("SEEONLINE_API_URL"),
        ALLOWED_USERS=list(map(int, os.getenv("ALLOWED_USERS", "").split(","))),
        REDIS_URL=os.getenv("REDIS_URL"),
    )


redis_states = Redis.from_url(f"{os.getenv("REDIS_URL")}/0")
redis_cache = Redis.from_url(f"{os.getenv("REDIS_URL")}/1")

storage = RedisStorage(redis=redis_states, key_builder=DefaultKeyBuilder(with_bot_id=True))
