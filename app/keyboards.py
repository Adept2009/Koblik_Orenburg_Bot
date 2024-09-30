from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Near-miss')],
                                     [KeyboardButton(text='О боте'),
                                      KeyboardButton(text='О компании')]],
                           resize_keyboard=True, one_time_keyboard=False,
                           input_field_placeholder='Выберите пункт меню...')  # Параметр resize_keyboard - отвечает
                                        # за более мелкий размер кнопок (True), параметр one_time_keyboard - отвечает
                                        # за то чтобы кнопки не пропадали, а сворачивались вниз (False)
