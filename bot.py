import asyncio
import signal
from aiogram import Bot, Dispatcher
from config import load_config, storage

# роутеры
## хендлеры
from handlers.base_commands import router as base_commands_router
from handlers.admin_panel import router as admin_panel_router
## каллбек обработчики
from callbacks.monitor_account_callbacks import router as monitor_account_callbacks_router
from callbacks.monitored_account_callbacks import router as monitored_account_callbacks_router
from callbacks.monitor_setting_callbacks import router as monitor_setting_callbacks_router
from callbacks.additional_callbacks import router as additional_callbacks_router
from callbacks.base_callbacks import router as base_callbacks_router

# мидлвари
from middleware import WhitelistMiddleware

# конфиг епта
config = load_config()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=storage, bot=bot)

# мидлвари
dp.message.middleware(WhitelistMiddleware(config.ALLOWED_USERS))
dp.callback_query.middleware(WhitelistMiddleware(config.ALLOWED_USERS))

dp.include_routers(
    base_commands_router,
    admin_panel_router,
    # smsbower_router,
    monitor_account_callbacks_router,
    monitored_account_callbacks_router,
    monitor_setting_callbacks_router,
    additional_callbacks_router,
    base_callbacks_router,
)


async def shutdown_trigger():
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)
    await stop_event.wait()


async def main():
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, shutdown_trigger=shutdown_trigger)

    print("Останавливаем бота...")

    try:
        dp.shutdown()
    except Exception as e:
        print("Ошибка при вызове dp.shutdown():", e)

    try:
        await asyncio.wait_for(bot.session.close(), timeout=10)
    except asyncio.TimeoutError:
        print("bot.session.close() завис, принудительно завершаем.")

    print("Бот остановлен.")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")
