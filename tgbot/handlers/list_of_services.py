from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from tgbot.keyboards.reply import callback_weight_of_pet, list_of_groomer_services, weight_of_pet_menu_for_groomer, \
    services_list, test
from tgbot.services.db_commands import search_groomer_for_mini_pet, search_groomer_for_middle_pet, search_groomer_for_big_pet


async def services_menu(call: CallbackQuery, callback_data: dict):
    weight_id = callback_data['weight_id']
    category = callback_data['category']
    await call.message.edit_reply_markup(reply_markup=await services_list(weight_id, category))

def register_list_of_services_for_groomer(dp: Dispatcher):
    dp.register_callback_query_handler(services_menu, test.filter(act='pet_weight'))

