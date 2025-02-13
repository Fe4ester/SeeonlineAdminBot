import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str
    SMSBOWER_API_URL: str
    SMSBOWER_TOKEN: str


def load_config() -> Config:
    return Config(
        BOT_TOKEN=os.getenv("BOT_TOKEN"),
        SMSBOWER_API_URL=os.getenv("SMSBOWER_API_URL"),
        SMSBOWER_TOKEN=os.getenv("SMSBOWER_TOKEN")
    )
