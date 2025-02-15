import asyncio
import signal
from aiogram import Bot, Dispatcher
from config import load_config
from handlers.base_commands import router as base_commands_router
from handlers.smsbower import router as smsbower_router

config = load_config()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

dp.include_routers(
    base_commands_router,
    # smsbower_router
)


async def shutdown_trigger():
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)
    await stop_event.wait()


async def main():
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
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
