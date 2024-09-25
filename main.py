import logging  # Для логирования на время отладки бота. ЗАТЕМ ОТКЛЮЧИТЬ ЛОГИРОВАНИЕ
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType, InputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# Импорт библиотек и модулей для отправки сообщений на e-mail
import smtplib

from os.path import basename

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import app.keyboards as kb

from config import TOKEN, CHAT_ID, FROM_EMAIL, TO_EMAIL, PASSWORD


bot = Bot(token=TOKEN)
dp = Dispatcher()


class SendNearMiss(StatesGroup):
    name = State()
    media = State()
    msg = State()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет!\nВаше имя: {message.from_user.first_name}\n'
                        f'Ваше имя пользователя: {message.from_user.username}\n'
                        f'Ваш ID: {message.from_user.id}', reply_markup=kb.main)


@dp.message(F.text == 'Near-miss')
async def near_miss_media(message: Message, state: FSMContext):
    await state.set_state(SendNearMiss.name)
    await message.answer('Для регистрации Near-Miss, укажите Имя и Фамилию')


@dp.message(SendNearMiss.name)
async def near_miss_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(SendNearMiss.media)
    await message.answer('Прикрепите фото ...')


@dp.message(SendNearMiss.media)
async def near_miss_msg(message: Message, state: FSMContext):
    await state.update_data(media=message.photo[-1].file_id)
    photo_file_id = message.photo[-1].file_id
    print(photo_file_id)
    name_file = f"tmp/{message.photo[-1].file_id}.jpg"
    await bot.download(message.photo[-1],
                       destination=name_file)  # Сохраняется в папку tmp в папке программы на компе/сервере
    await state.set_state(SendNearMiss.msg)
    await message.answer('Спасибо за фото. Напишите комментарии, пояснения к данному фото ...')


@dp.message(SendNearMiss.msg)
async def near_miss_content(message: Message, state: FSMContext):
    await state.update_data(msg=message.text)
    data = await state.get_data()
    print(data)
    await message.answer('Спасибо за участие в мероприятиях по безопасному производству')
    title = f'<b>NEAR-MISS от {data["name"]}.</b>'
    await bot.send_message(chat_id=CHAT_ID,
                           text=title,
                           parse_mode='HTML')
    await bot.send_photo(chat_id=CHAT_ID, photo=data["media"])
    await bot.send_message(chat_id=CHAT_ID, text=data["msg"])

    photo_file_id = data["media"]
    print(photo_file_id)
    name_file = f"tmp/{photo_file_id}.jpg"
    # await bot.download(message.photo[-1],
    #                    destination=name_file)  # Сохраняется в папку tmp в папке программы на компе/сервере

    # Отправка на e-mail
    # Надо сохранять файлы на комп/сервер, а после отправки на e-mail удалять (чтобы не занимать место)
    # А в последствии надо реализовать проверку, чтобы удалять файлы только после того, как пришел ответ от
    # почтового сервера, что письмо доставлено.
    from_email = FROM_EMAIL
    to_email = TO_EMAIL
    subject = title[3:-4]   # Добавил срез для удаления HTML разметки, разметка добавлена для заголовка в ТГ

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email)     # Для отправки списком (несколько получателеЙ) ОБЯЗАТЕЛЬНО сделать через join
    msg['Subject'] = subject

    # Подготовка картинки к отправке
    with open(name_file, "rb") as media:
        file = MIMEApplication(media.read(), Name=basename("file.jpg"))

    # Отправка картинки
    msg.attach(file)
    # Отправка текста
    msg.attach(MIMEText(message.text))

    with smtplib.SMTP('smtp.yandex.ru', 587) as smtp:
        smtp.starttls()
        smtp.login(from_email, PASSWORD)
        smtp.sendmail(from_email, to_email, msg.as_string())
        # smtp.send_message(msg)
        smtp.quit()

    await state.clear()


    # @dp.message(F.photo)
    # async def get_photo(message: Message):
    #     await message.reply('Спасибо за фото. Напишите комментарии, пояснения к данному фото ...')
    #     photo_file_id = message.photo[-1].file_id
    #     print(photo_file_id)
    #     name_file = f"tmp/{message.photo[-1].file_id}.jpg"
    #     await bot.download(message.photo[-1],
    #                        destination=name_file)  # Сохраняется в папку tmp в папке программы на компе/сервере
    #
    #     @dp.message(F.text)
    #     async def get_text(message: Message):
    #         await message.reply('Спасибо за участие в мероприятиях по безопасному производству')
    #         await bot.send_message(chat_id=CHAT_ID,
    #                                text='<b>NEAR-MISS</b>',
    #                                parse_mode='HTML')   # Как вариант сообщение надо сделать формата:
    #                                                                     # 'NEAR-MISS от Ф.И.О. и № телефона'
    #         await bot.send_photo(chat_id=CHAT_ID, photo=photo_file_id)
    #         await bot.send_message(chat_id=CHAT_ID, text=message.text)
    #
    #         # Отправка на e-mail
    #         # Надо сохранять файлы на комп/сервер, а после отправки на e-mail удалять (чтобы не занимать место)
    #         # А в последствии надо реализовать проверку, чтобы удалять файлы только после того, как пришел ответ от
    #         # почтового сервера, что письмо доставлено.
    #         from_email = FROM_EMAIL
    #         to_email = TO_EMAIL
    #         subject = 'Near-miss от ...'
    #
    #         msg = MIMEMultipart()
    #         msg['From'] = from_email
    #         msg['To'] = ', '.join(to_email) # Для отправки списком (несколько получателеЙ) ОБЯЗАТЕЛЬНО сделать через join
    #         msg['Subject'] = subject
    #
    #         # Подготовка картинки к отправке
    #         with open(name_file, "rb") as media:
    #             file = MIMEApplication(media.read(), Name=basename("file.jpg"))
    #
    #         # Отправка картинки
    #         msg.attach(file)
    #         # Отправка текста
    #         msg.attach(MIMEText(message.text))
    #
    #         with smtplib.SMTP('smtp.yandex.ru', 587) as smtp:
    #             smtp.starttls()
    #             smtp.login(from_email, PASSWORD)
    #             smtp.sendmail(from_email, to_email, msg.as_string())
    #             # smtp.send_message(msg)
    #             smtp.quit()

    # await state.clear


@dp.message(F.text == 'О боте')
async def about_us(message: Message):
    await message.answer('Для отображения кнопок бота набрать и отправить сообщение - /start\n\n'
                         'Бот предоставляет возможность отправить фотографию или видео,'
                         ' а также комментарии к ним для предотвращения негативного развития событий.')


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
