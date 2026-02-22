from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def simple_kb(buttons):
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def start_excursion_kb():
    return simple_kb([[InlineKeyboardButton(text="▶️ Начать экскурсию", callback_data="start_trip")]])

def im_here_kb():
    return simple_kb([[InlineKeyboardButton(text="📍 Я на месте", callback_data="im_here")]])

def next_kb():
    return simple_kb([[InlineKeyboardButton(text="➡️ Готов двигаться дальше", callback_data="next")]])

def home_kb():
    return simple_kb([[InlineKeyboardButton(text="🏠 В меню", callback_data="home")]])
