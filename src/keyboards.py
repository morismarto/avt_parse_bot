from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from src.city_list import cities

start_kb = ReplyKeyboardMarkup(
        keyboard=[
        [KeyboardButton(text='Найти процессоры')], 
        [KeyboardButton(text='Выбрать город')]
        ], 
        resize_keyboard=True)


cities_kb = InlineKeyboardMarkup(inline_keyboard=
        [[InlineKeyboardButton(text=i[0], callback_data=i[1])] for i in cities.items()])