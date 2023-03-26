from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from tgbot.keyboards.inline import callback_start_menu, pet_weight, callback_weight_of_pet


async def weight_pet_menu(call: CallbackQuery, callback_data: dict):
    category = callback_data['category_id']
    await call.message.edit_reply_markup(reply_markup=await pet_weight(category))


async def back_to_weight_menu(call: CallbackQuery, callback_data: dict):
    category = callback_data['category']
    await call.message.edit_reply_markup(reply_markup=await pet_weight(category))


def register_weight_menu(dp: Dispatcher):
    dp.register_callback_query_handler(weight_pet_menu, callback_start_menu.filter(act='category'))
    dp.register_callback_query_handler(back_to_weight_menu, callback_weight_of_pet.filter(act='back_to_weight'))

