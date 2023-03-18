from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from tgbot.config import load_config
from tgbot.keyboards.reply import menu_admin, menu_user, callback_start_menu


async def start_menu(message: Message):
    user = message.from_user.id
    config = load_config('.env').tg_bot.admin_ids
    admins = [admin for admin in config]

    if user in admins:
        await message.answer(text=f'Привет, {message.from_user.full_name}!\n'
                                  f'Время заботы \u2764'+'\n'
                                  f'Выбери к кому хочешь записаться \U0001F447', reply_markup=menu_admin())
    else:
        await message.answer(text=f'Привет, {message.from_user.full_name}!\n'
                                  f'Время заботы \u2764'+'\n'
                                  f'Выбери к кому хочешь записаться \uE22F', reply_markup=menu_user())


async def back_to_menu(call: CallbackQuery):
    user = call.from_user.id
    config = load_config('.env').tg_bot.admin_ids
    admins = [admin for admin in config]
    if user in admins:
        await call.message.edit_reply_markup(reply_markup=menu_admin())
    else:
        await call.message.edit_reply_markup(reply_markup=menu_user())


def register_start_menu(dp: Dispatcher):
    dp.register_message_handler(start_menu, commands=["menu"], state="*")
    dp.register_callback_query_handler(back_to_menu, callback_start_menu.filter(key='back_to_menu'))

