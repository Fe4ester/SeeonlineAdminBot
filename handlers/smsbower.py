from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.smsbower_api import SmsBowerAPI

from config import load_config
from services.countries import countries

router = Router()

config = load_config()


@router.message(Command('smsbower'))
async def cmd_smsbower(message: Message):
    # Баланс
    api = SmsBowerAPI(config.SMSBOWER_API_URL)
    balance = await api.get_balance(config.SMSBOWER_TOKEN)

    await message.answer(f"""
Текущий баланс: {balance}
Удачи поторговаться в этой ебаной колымаге

Работа чисто с командами - /smsbower_commands
""")


@router.message(Command('get_prices'))
async def cmd_get_prices(message: Message):
    api = SmsBowerAPI(config.SMSBOWER_API_URL)

    data = await api.get_prices(config.SMSBOWER_TOKEN)

    result = []
    for country_id, details in data.items():
        country_name = countries.get(int(country_id), "Unknown Country")
        cost = details["tg"]["cost"]
        count = details["tg"]["count"]
        result.append(f"({country_id}) {country_name}: {cost} - {count}")

    prices = "\n".join(result)

    await message.answer(prices)


@router.message(Command('get_balance'))
async def cmd_get_balance(message: Message):
    api = SmsBowerAPI(config.SMSBOWER_API_URL)

    balance = await api.get_balance(config.SMSBOWER_TOKEN)

    await message.answer(f"Баланс епта: {balance}")


@router.message(Command('smsbower_commands'))
async def cmd_smsbower_commands(message: Message):
    await message.answer("""
/get_balance - Баланс
/get_prices - Лист номеров и цен
""")
