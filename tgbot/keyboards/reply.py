from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_menu = KeyboardButton('/menu')
admin_help = KeyboardButton('/help')
admin_keyboard.add(admin_menu, admin_help)
state_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
state_cancel = KeyboardButton('/cancel')
state_keyboard.add(state_cancel)