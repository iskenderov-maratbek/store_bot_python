from aiogram import Dispatcher
from aiogram.types import Message
from tgbot.keyboards.inline import user_store
from tgbot.database import sqlite_db


async def user_start(msg: Message):
    await msg.reply(f"Добро пожаловать, пользователь {msg.from_user.username}\nРекомендую прямо сейчас нажать help и узнать о возможностях нашего бота)\n P.S. Если же вы уже знакомы, можете сразу нажимать на /menu в меню управления",
        reply_markup=user_store)


async def product_list(msg: Message):
    await sqlite_db.sql_read(msg)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state=None)
