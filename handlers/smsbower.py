from aiogram import Router
from aiogram.types import Message

from aiogram.filters import Command

from services.smsbower_api import SmsBowerAPI

router = Router()

@router.message(Command('smsbower'))
async def cmd_smsbower(message: Message):
    pass

@router.message(Command('api_test'))
async def cmd_api_test(message: Message):
    """
    Показываем, как вызывать внешний API из бота.
    Допустим, вы хотели получить какие-то данные, например /todos/1.
    """
    # Создаём экземпляр класса ExternalAPI прямо тут или получаем откуда-то DI
    api = SmsBowerAPI("https://jsonplaceholder.typicode.com")

    data = await api.get_data("/todos/1")
    # data будет словарём: {"userId":..., "id":..., "title":..., "completed":...}

    # Формируем текст ответа
    user_id = data.get("userId")
    title = data.get("title")
    completed = data.get("completed")

    text = (f"Данные из внешнего API:\n"
            f"UserID: {user_id}\n"
            f"Title: {title}\n"
            f"Completed: {completed}")

    await message.answer(text)
