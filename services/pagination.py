from aiogram.types import CallbackQuery

# клавиатуры
from keyboards.inline_kb import get_pagination_keyboard

# сервисы
from services.api_services.seeonline_api import SeeOnlineAPI

# доп.
import json
import math

# конфиг
from config import redis_cache, load_config

config = load_config()

# скорее всего костыль тк делал через гпт
# todo пересмотреть, рефакторить, гпт
async def show_monitor_accounts_page(
        callback: CallbackQuery,
        page: int,
        page_size: int,
        ttl: int,
        edit: bool = False
):
    """
    Отображает нужную страницу списка аккаунтов, загружая или беря из Redis.
    Если Redis не имеет свежих данных, то идёт запрос в API.
    """
    user_id = callback.from_user.id
    redis_key = f"monitor_accounts:{user_id}"

    # Пытаемся считать кэш из Redis
    data = await redis_cache.get(redis_key)
    if data:
        try:
            monitor_accounts = json.loads(data)
        except json.JSONDecodeError:
            monitor_accounts = None
    else:
        monitor_accounts = None

    if not monitor_accounts:
        # Данных в Redis нет либо они невалидны — грузим из API
        api = SeeOnlineAPI(config.SEEONLINE_API_URL)
        monitor_accounts = await api.get_monitor_account()
        # Сохраняем с TTL
        await redis_cache.set(redis_key, json.dumps(monitor_accounts), ex=ttl)

    # Если список аккаунтов всё равно пуст
    if not monitor_accounts:
        text = "📭 Список аккаунтов пуст."
        if edit:
            await callback.message.edit_text(text)
        else:
            await callback.message.answer(text)
        return await callback.answer()

    # Подсчёт страниц
    total_items = len(monitor_accounts)
    total_pages = math.ceil(total_items / page_size)

    # Корректируем page, если выходим за границы
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    # Берём нужные аккаунты
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    current_page_items = monitor_accounts[start_idx:end_idx]

    # Формируем текст
    text = (
        f"📋 <b>Список мониторинговых аккаунтов</b> "
        f"(страница {page}/{total_pages}):\n\n"
    )
    for account in current_page_items:
        text += (
            f"🔹 <b>ID:</b> {account['id']}\n"
            f"👤 <b>User ID:</b> <code>{account['user_id']}</code>\n"
            f"🆔 <b>API ID:</b> <code>{account['api_id']}</code>\n"
            f"🔑 <b>API Hash:</b> <code>{account['api_hash']}</code>\n"
            f"✅ <b>Активен:</b> {'Да' if account['is_active'] else 'Нет'}\n"
            f"🔐 <b>Авторизован:</b> {'Да' if account['is_auth'] else 'Нет'}\n"
            f"🕒 <b>Создан:</b> {account['created_at']}\n"
            f"🔄 <b>Обновлён:</b> {account['updates_at']}\n"
            "────────────────────────\n"
        )

    # Генерируем клавиатуру пагинации
    pagination_kb = get_pagination_keyboard(page, total_pages)

    if edit:
        # Редактируем текущее сообщение
        await callback.message.edit_text(text, reply_markup=pagination_kb, parse_mode="HTML")
    else:
        # Отправляем новое сообщение
        await callback.message.answer(text, reply_markup=pagination_kb, parse_mode="HTML")

    await callback.answer()
