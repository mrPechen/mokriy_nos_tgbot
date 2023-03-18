from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.config import load_config
from tgbot.keyboards.reply import menu_admin, menu_user
from tgbot.services import db_commands


async def user_start(message: Message):

    user_in_db = await db_commands.select_user(user_id=message.from_user.id)

    if user_in_db:
        await message.answer("Для вызова меню нажми /menu")
    else:
        await db_commands.add_user(user_id=message.from_user.id,
                                   full_name=message.from_user.full_name,
                                   username=message.from_user.username)
        user = message.from_user.id
        config = load_config('.env').tg_bot.admin_ids
        admins = [admin for admin in config]
        if user in admins:
            await message.answer(text=f'Привет, {message.from_user.full_name}!\n'
                                      f'Время заботы \u2764' + '\n'
                                                               f'Выбери к кому хочешь записаться \U0001F447',
                                 reply_markup=menu_admin())
        else:
            await message.answer(text=f'Привет, {message.from_user.full_name}!\n'
                                      f'Время заботы \u2764' + '\n'
                                                               f'Выбери к кому хочешь записаться \uE22F',
                                 reply_markup=menu_user())


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")