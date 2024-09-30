import logging  # Для логирования на время отладки бота. ЗАТЕМ ОТКЛЮЧИТЬ ЛОГИРОВАНИЕ
import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router

# Импорт библиотеки для создания и работы с файлом .env (для хранения конфиденциальной информации)
from dotenv import load_dotenv

from config import TOKEN

bot = Bot(token=TOKEN)


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)     # Для логирования на время отладки бота. ЗАТЕМ ОТКЛЮЧИТЬ ЛОГИРОВАНИ
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен!')
