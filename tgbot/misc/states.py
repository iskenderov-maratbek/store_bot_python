from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.database import sqlite_db
from tgbot.keyboards.reply import state_keyboard, admin_keyboard


class AddToDatabase(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


def cancel(cmd):
    if cmd == "/cancel":
        return True
    return False


async def load_image(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data["image"] = msg.photo[0].file_id
    await AddToDatabase.next()
    await msg.reply("Введите название продукта:", reply_markup=state_keyboard)


async def load_name(msg: Message, state: FSMContext):
    if cancel(msg.text): await tip_cancel_state(msg, state)
    async with state.proxy() as data:
        data["name"] = msg.text
    await AddToDatabase.next()
    await msg.reply("Введите описание продукта:", reply_markup=state_keyboard)


async def load_description(msg: Message, state: FSMContext):
    if cancel(msg.text): await tip_cancel_state(msg, state)
    async with state.proxy() as data:
        data["description"] = msg.text
    await AddToDatabase.next()
    await msg.reply("Укажите цену продукта", reply_markup=state_keyboard)


async def load_price(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data["price"] = msg.text
    await sqlite_db.sql_add(state)
    await state.finish()
    await msg.answer("Загрузка...", reply_markup=ReplyKeyboardRemove())
    await msg.bot.delete_message(msg.chat.id, msg.message_id)
    await msg.answer("Продукт успешно добавлен! ✅", reply_markup=admin_keyboard)


async def tip_cancel_state(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        if msg.text != "/cancel":
            await msg.answer(
                "Вы в режиме добавления продукта! Для выхода из режима введите или нажмите '/cancel' в меню управления",
                reply_markup=state_keyboard)
        else:
            await state.finish()
            await msg.answer(
                "Добавление продукта отменено! ❌",
                reply_markup=admin_keyboard)


def register_states(dp: Dispatcher):
    dp.register_message_handler(load_image, content_types=['photo'], state=AddToDatabase.photo,
                                is_admin=True)
    dp.register_message_handler(load_name, content_types=['text'], state=AddToDatabase.name,
                                is_admin=True)
    dp.register_message_handler(load_description, content_types=['text'],
                                state=AddToDatabase.description,
                                is_admin=True)
    dp.register_message_handler(load_price, content_types=['text'], state=AddToDatabase.price,
                                is_admin=True)
    dp.register_message_handler(tip_cancel_state, content_types=['text'], state="*", is_admin=True)
