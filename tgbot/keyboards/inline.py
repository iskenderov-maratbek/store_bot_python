from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from unicodedata import category

# ----------Меню администратора--------------------
# Управление продуктами
product_controller = InlineKeyboardMarkup(row_width=2)
add_product = InlineKeyboardButton('Добавить товар', callback_data='add_product')
edit_product = InlineKeyboardButton('Изменить товар', callback_data='edit_product')
delete_product = InlineKeyboardButton('Удалить товар', callback_data='delete_product')

print_product = InlineKeyboardButton('Список всех товаров', callback_data='list_product')
product_controller.add(add_product, edit_product, delete_product)
product_controller.add(print_product)

# -----------Меню пользователя--------------------------------
# Просмотр продуктов
user_store = InlineKeyboardMarkup(row_width=2)
support = InlineKeyboardButton('Поддержка', callback_data='support')
about = InlineKeyboardButton('О программе', callback_data='about')
categories = InlineKeyboardButton('Категории', callback_data='categories')
categories_data = {}
user_store.add(support, about, categories)
