from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from tgbot.keyboards.inline import product_controller
from tgbot.keyboards.reply import admin_keyboard,state_keyboard
from tgbot.database import sqlite_db
from tgbot.misc.states import AddToDatabase


# Команда /start для администратора
async def admin_start(msg: Message):
    await msg.reply(f"Здравсвтуйте, администатор {msg.from_user.first_name}", reply_markup=admin_keyboard)


# Команда /help для администратора
async def admin_help(msg: Message):
    await msg.answer("Инструкция для администратора\n"
                     "1. /start - для запуска бота\n"
                     "2. /help - для вызова инструкции\n"
                     "3. /menu - вызов меню управления продуктами\n"
                     "P.S. Также вы можете выбрать действие из меню управления")


# Команда /menu для администратора
async def admin_menu(msg: Message):
    await msg.answer("Выберите действие:", reply_markup=product_controller)


async def state_start(call: CallbackQuery):
    # Добавление в базу данных
    if call.data == "add_product":
        await AddToDatabase.photo.set()
        await call.message.answer("Загрузите фото продукта:", reply_markup=state_keyboard)

    # Список в базе данных
    if call.data == "list_product":
        await sqlite_db.sql_read(call)

    # Удаление из базы данных
    if call.data == "delete_product":
        await sqlite_db.sql_delete(call)


# Команда для регистрации всех событий администраторов
def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state=None, is_admin=True)
    dp.register_message_handler(admin_help, commands=["help"], state=None, is_admin=True)
    dp.register_message_handler(admin_menu, commands=["menu"], state=None, is_admin=True)
    dp.register_callback_query_handler(state_start, state=None, is_admin=True)
