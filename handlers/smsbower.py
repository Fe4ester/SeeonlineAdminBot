from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import load_config
from services.countries import countries
from services.smsbower_api import SmsBowerAPI

router = Router()
config = load_config()


def parse_named_params(args: list, defaults: dict) -> dict:
    """
    Парсит аргументы вида key:value и возвращает словарь с параметрами,
    используя значения по умолчанию из defaults.
    """
    params = defaults.copy()
    for arg in args:
        if ':' in arg:
            key, value = arg.split(":", 1)
            key = key.lower().strip()
            value = value.strip()
            if key in params:
                params[key] = value
    return params


def format_api_error(e: Exception) -> str:
    return f"Ошибка: {e}\n"


@router.message(Command('get_prices'))
async def cmd_get_prices(message: Message):
    args = message.text.split()[1:]
    defaults = {
        "v": "1",
        "c": None,
        "mp": "40",
        "mc": "5"
    }
    params = parse_named_params(args, defaults)

    try:
        version = int(params["v"])
        country = int(params["c"]) if params["c"] is not None else None
        max_price = float(params["mp"])
        min_count = int(params["mc"])
    except ValueError:
        await message.answer(
            "Неверный формат аргументов. Пример использования: /get_prices v:1 c:31 mp:30 mc:10"
        )
        return

    api = SmsBowerAPI(config.SMSBOWER_API_URL)
    try:
        data = await api.get_prices(
            config.SMSBOWER_TOKEN,
            country=country,
            version=version,
            max_price=max_price,
            min_count=min_count
        )
    except ValueError as e:
        await message.answer(format_api_error(e))
        return

    # Формируем вывод в зависимости от версии API
    if version == 1:
        result = []
        for country_id, details in data.items():
            country_name = countries.get(int(country_id), "Unknown Country")
            cost = details["tg"]["cost"]
            count = details["tg"]["count"]
            result.append(
                f"🌍 <b>{country_name}</b> ({country_id}):\n"
                f"💰 {cost} руб. — 📦 {count} шт."
            )
        prices_message = "\n\n".join(result)
        await message.answer(prices_message, parse_mode="HTML")

    elif version == 2:
        result = []
        for country_id, details in data.items():
            country_name = countries.get(int(country_id), "Unknown Country")
            prices_list = details["tg"]

            if len(prices_list) == 1:
                # Если в списке только один вариант цены
                price, count = next(iter(prices_list.items()))
                result.append(
                    f"🌍 <b>{country_name}</b> ({country_id}):\n"
                    f"💰 {price} руб. — 📦 {count} шт."
                )
            else:
                # Если цен несколько
                prices_block = "\n".join(
                    f"    💰 {price} руб. — 📦 {count} шт."
                    for price, count in prices_list.items()
                )
                result.append(f"🌍 <b>{country_name}</b> ({country_id}):\n{prices_block}")
        prices_message = "\n\n".join(result)
        await message.answer(prices_message, parse_mode="HTML")
    else:
        await message.answer("Неверная версия. Используйте v:1 или v:2.")


@router.message(Command('get_number'))
async def cmd_get_number(message: Message):
    args = message.text.split()[1:]
    defaults = {"mp": "40", "c": "31", "pids": None, "excpids": None}
    params = parse_named_params(args, defaults)

    try:
        max_price = float(params["mp"])
        country = int(params["c"])
        provider_ids = params["pids"]
        except_provider_ids = params["excpids"]
    except ValueError:
        await message.answer(
            "Неверный формат аргументов. Пример использования: /get_number mp:40 c:31 pids:1,2 excpids:3"
        )
        return

    api = SmsBowerAPI(config.SMSBOWER_API_URL)
    try:
        data = await api.get_number(
            config.SMSBOWER_TOKEN,
            max_price=max_price,
            country=country,
            provider_ids=provider_ids,
            except_provider_ids=except_provider_ids
        )
    except ValueError as e:
        await message.answer(format_api_error(e))
        return

    country_name = countries.get(int(data["countryCode"]), "Unknown Country")
    activation_cost = data["activationCost"]
    activation_id = data["activationId"]
    phone_number = data["phoneNumber"]
    activation_time = data["activationTime"]
    can_get_sms = "✅ Да" if data["canGetAnotherSms"] == "1" else "❌ Нет"

    formatted_message = (
        f"📲 <b>Новый номер для активации</b>\n"
        f"🌍 Страна: {country_name} ({data['countryCode']})\n"
        f"📞 Номер: <code>{phone_number}</code>\n"
        f"💰 Стоимость: {activation_cost} руб.\n"
        f"⏳ Время активации: {activation_time}\n"
        f"📩 Можно получить еще SMS: {can_get_sms}\n"
        f"🆔 ID активации: <code>{activation_id}</code>"
    )
    await message.answer(formatted_message, parse_mode="HTML")


@router.message(Command('get_sms'))
async def cmd_get_sms(message: Message):
    args = message.text.split()[1:]
    if not args:
        await message.answer("⚠️ Параметр activation_id обязателен!")
        return

    activation_id = args[0]
    api = SmsBowerAPI(config.SMSBOWER_API_URL)

    try:
        data = await api.get_sms(config.SMSBOWER_TOKEN, activation_id)
    except ValueError as e:
        await message.answer(format_api_error(e))
        return

    await message.answer(data)


@router.message(Command('set_status'))
async def cmd_set_status(message: Message):
    args = message.text.split()[1:]
    if not args:
        await message.answer(
            "⚠️ Параметр activation_id обязателен!\n\n"
            "Доступные именованные параметры:\n"
            "  aid – activation_id\n"
            "  s – status (допустимые значения: 1, 3, 6, 8)\n\n"
            "Попробуйте снова, указав нужные параметры."
        )
        return

    defaults = {"aid": None, "s": None}
    params = parse_named_params(args, defaults)

    if not params["aid"]:
        await message.answer(
            "⚠️ Параметр activation_id обязателен!\n\n"
            "Доступные именованные параметры:\n"
            "  aid – activation_id\n"
            "  s – status (допустимые значения: 1, 3, 6, 8)\n\n"
            "Пожалуйста, проверьте и повторите попытку."
        )
        return

    if not params["s"]:
        await message.answer(
            "⚠️ Параметр status обязателен!\n\n"
            "Доступные именованные параметры:\n"
            "  aid – activation_id\n"
            "  s – status (допустимые значения: 1, 3, 6, 8)\n\n"
            "Попробуйте снова, указав оба параметра."
        )
        return

    allowed_statuses = {"1", "3", "6", "8"}
    if params["s"] not in allowed_statuses:
        await message.answer(
            "⚠️ Неверное значение параметра status!\n\n"
            "Доступные именованные параметры:\n"
            "  aid – activation_id\n"
            "  s – статус активации (допустимые значения: 1, 3, 6, 8)\n\n"
            "Пожалуйста, укажите корректное значение для status."
        )
        return

    api = SmsBowerAPI(config.SMSBOWER_API_URL)
    try:
        result = await api.set_status(config.SMSBOWER_TOKEN, params["aid"], params["s"])
        await message.answer(f"Статус изменен: {result}", parse_mode="HTML")
    except Exception as e:
        await message.answer(format_api_error(e), parse_mode="HTML")


@router.message(Command('get_balance'))
async def cmd_get_balance(message: Message):
    api = SmsBowerAPI(config.SMSBOWER_API_URL)
    try:
        balance = await api.get_balance(config.SMSBOWER_TOKEN)
    except ValueError as e:
        await message.answer(format_api_error(e))
        return

    formatted_message = (
        f"💰 <b>Баланс</b>\n"
        f"📊 Текущий баланс: <b>{balance} руб.</b>\n"
        f"🔄 Обновлено в реальном времени."
    )
    await message.answer(formatted_message, parse_mode="HTML")


@router.message(Command('smsbower'))
async def cmd_smsbower(message: Message):
    api = SmsBowerAPI(config.SMSBOWER_API_URL)
    balance = await api.get_balance(config.SMSBOWER_TOKEN)

    formatted_message = (
        f"💰 <b>Текущий баланс:</b> <code>{balance} руб.</code>\n\n"
        f"📢 Удачи поторговаться в этой ебаной колымаге\n\n"
        f"📜 <b>Доступные команды:</b>\n\n"
        f"💰 /get_balance — Проверить баланс\n"
        f"📊 /get_prices — Лист цен (параметры в /smsbower_docs)\n"
        f"📞 /get_number — Купить номер (⚠️ Внимательно все проверять!)\n"
        f"📩 /get_sms — Получить смс (передаем activation_id)\n"
        f"🔧 /set_status — Установить статус активации (параметры: aid, s)\n\n"
        f"📄 /smsbower_docs — Документация по работе с API"
    )

    await message.answer(formatted_message, parse_mode="HTML")


@router.message(Command('smsbower_docs'))
async def cmd_smsbower_docs(message: Message):
    docs_message = (
        "<b>📜 Документация SmsBower API</b>\n\n"
        "<b>🔍 Обзор:</b>\n"
        "Этот бот предоставляет доступ к API сервиса <b>SmsBower</b>, позволяя:\n"
        "✅ Проверять баланс\n"
        "✅ Получать список цен\n"
        "✅ Покупать номера\n"
        "✅ Получать СМС-коды\n"
        "✅ Управлять статусами активаций\n\n"
        "<b>⚙️ Команды:</b>\n"
        "🔹 <b>/get_balance</b> — Проверка текущего баланса.\n"
        "   📌 Пример: <code>/get_balance</code>\n\n"
        "🔹 <b>/get_prices</b> — Получение списка цен для сервиса 'tg'.\n"
        "   🔧 <b>Параметры:</b>\n"
        "   - <code>v</code>: версия API (1 или 2). По умолчанию: 1.\n"
        "   - <code>c</code>: код страны (необязательно).\n"
        "   - <code>mp</code>: макс. цена. По умолчанию: 40.\n"
        "   - <code>mc</code>: мин. количество номеров. По умолчанию: 5.\n"
        "   📌 Пример: <code>/get_prices v:1 c:31 mp:30 mc:10</code>\n\n"
        "🔹 <b>/get_number</b> — Покупка нового номера для активации.\n"
        "   🔧 <b>Параметры:</b>\n"
        "   - <code>mp</code>: макс. цена. По умолчанию: 40.\n"
        "   - <code>c</code>: код страны. По умолчанию: 31.\n"
        "   - <code>pids</code>: провайдеры (ID через запятую).\n"
        "   - <code>excpids</code>: исключённые провайдеры (ID через запятую).\n"
        "   📌 Пример: <code>/get_number mp:40 c:31 pids:1,2 excpids:3</code>\n\n"
        "🔹 <b>/get_sms</b> — Получение СМС-кода по номеру.\n"
        "   🔧 <b>Параметры:</b>\n"
        "   - <code>activation_id</code>: ID активации.\n"
        "   📌 Пример: <code>/get_sms 123456</code>\n\n"
        "🔹 <b>/set_status</b> — Управление статусом активации.\n"
        "   🔧 <b>Параметры:</b>\n"
        "   - <code>aid</code>: ID активации.\n"
        "   - <code>s</code>: статус (1, 3, 6, 8 — см. описание ниже).\n"
        "   📌 Пример: <code>/set_status aid:123456 s:6</code>\n\n"
        "<b>📌 Описание статусов активаций:</b>\n"
        "🔹 <b>1</b> — <i>SMS отправлена</i> (необязательно, просто подтверждает отправку кода).\n"
        "🔹 <b>3</b> — <i>Запросить повторное SMS</i> (если код не пришел или некорректен).\n"
        "🔹 <b>6</b> — <i>Завершить активацию</i> (подтвердить получение кода и завершить процесс).\n"
        "🔹 <b>8</b> — <i>Отмена активации</i> (если номер не подошел или передумали).\n\n"
        "<b>📊 Хронология работы с API:</b>\n"
        "1️⃣ <b>Получение номера:</b>\n"
        "   - Используйте команду <code>/get_number</code>.\n"
        "   - Если номер не подошел, отмените активацию (<code>/set_status aid:XXX s:8</code>).\n\n"
        "2️⃣ <b>Ожидание SMS:</b>\n"
        "   - Можно подтвердить, что SMS отправлена (<code>/set_status aid:XXX s:1</code>), но это не обязательно.\n"
        "   - Если SMS не пришла, можно запросить повторную (<code>/set_status aid:XXX s:3</code>).\n\n"
        "3️⃣ <b>Завершение активации:</b>\n"
        "   - Как только получите код, завершите активацию (<code>/set_status aid:XXX s:6</code>).\n"
        "   - Если передумали, можно отменить активацию (<code>/set_status aid:XXX s:8</code>).\n\n"
        "<b>📌 Важно:</b>\n"
        "⚠️ Все команды должны вызываться с корректными параметрами.\n"
        "⚠️ При ошибках бот сообщит вам об этом.\n"
        "⚠️ Для работы с API необходим действующий API-ключ.\n\n"
        "📍 Для полного списка команд используйте <b>/smsbower</b>.\n"
        "❓ По вопросам обращайтесь: @Fe4ester"
    )
    await message.answer(docs_message, parse_mode="HTML")
