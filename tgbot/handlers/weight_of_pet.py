from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from tgbot.keyboards.reply import weight_of_pet_menu_for_groomer, callback_start_menu, weight_of_pet_menu_for_vet


async def weight_pet_menu_vet(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=weight_of_pet_menu_for_vet())


async def weight_pet_menu_groomer(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=weight_of_pet_menu_for_groomer())


def register_weight_menu(dp: Dispatcher):
    dp.register_callback_query_handler(weight_pet_menu_vet, callback_start_menu.filter(key='vetdoc'))
    dp.register_callback_query_handler(weight_pet_menu_groomer, callback_start_menu.filter(key='groomer'))

