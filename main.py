import logging  # Для логирования на время отладки бота. ЗАТЕМ ОТКЛЮЧИТЬ ЛОГИРОВАНИ
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType, InputFile
from aiogram.filters import CommandStart, Command

import app.keyboards as kb

from config import TOKEN, CHAT_ID


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет!\nВаше имя: {message.from_user.first_name}\n'
                        f'Ваше имя пользователя: {message.from_user.username}\n'
                        f'Ваш ID: {message.from_user.id}', reply_markup=kb.main)


@dp.message(F.text == 'Near-miss')
async def near_miss(message: Message):
    await message.answer('Прикрепите фото или видео ...')

    @dp.message(F.photo)
    async def get_photo(message: Message):
        await message.reply('Спасибо за фото. Напишите комментарии, пояснения к данному фото ...')
        photo_file_id = message.photo[-1].file_id
        print(photo_file_id)

        @dp.message(F.text)
        async def get_text(message: Message):
            await message.reply('Спасибо за участие в мероприятиях по безопасному производству')
            await bot.send_message(chat_id=CHAT_ID,
                                   text='<b>NEAR-MISS</b>',
                                   parse_mode='HTML')   # Как вариант сообщение надо сделать формата:
                                                                        # 'NEAR-MISS от Ф.И.О. и № телефона'
            await bot.send_photo(chat_id=CHAT_ID, photo=photo_file_id)
            await bot.send_message(chat_id=CHAT_ID, text=message.text)


@dp.message(F.text == 'О нас')
async def about_us(message: Message):
    await message.answer('Коблик Оренбург входит в состав KOBLIK GROUP.\n'
                         'KOBLIK GROUP – объединяет четыре агромашиностроительных предприятия'
                         ' и собственную сеть дилерских центров более чем в 20 регионах России. '
                         'Крупнейший отечественный производитель элеваторного оборудования и прицепной'
                         ' техники для операций на комплексах КРС.')


# @dp.message(Command('help'))
# async def cmd_help(message: Message):
#     await message.answer('Вы нажали на кнопку помощи')
#
#
# @dp.message(F.text == 'У меня все хорошо')
# async def nice(message: Message):
#     await message.answer('Я очень рад')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)     # Для логирования на время отладки бота. ЗАТЕМ ОТКЛЮЧИТЬ ЛОГИРОВАНИ
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен!')
