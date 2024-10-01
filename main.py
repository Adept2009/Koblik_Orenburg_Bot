import logging  # Для логирования на время отладки бота. ЗАТЕМ ОТКЛЮЧИТЬ ЛОГИРОВАНИЕ
import os
import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router

# Импорт библиотеки для создания и работы с файлом .env (для хранения конфиденциальной информации)
from dotenv import load_dotenv

bot = Bot(token=os.getenv('TOKEN'))


async def main():
    load_dotenv()
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)     # Для логирования на время отладки бота. ЗАТЕМ ОТКЛЮЧИТЬ ЛОГИРОВАНИ
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен!')
