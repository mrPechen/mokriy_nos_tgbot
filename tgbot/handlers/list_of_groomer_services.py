from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from tgbot.keyboards.reply import callback_weight_of_pet, list_of_groomer_services, weight_of_pet_menu_for_groomer
from tgbot.services.db_commands import search_groomer_for_mini_pet, search_groomer_for_middle_pet, search_groomer_for_big_pet


async def groomer_list_of_service_for_mini(call: CallbackQuery):
    services = await search_groomer_for_mini_pet()
    await call.message.edit_reply_markup(reply_markup=list_of_groomer_services(services))


async def groomer_list_of_service_for_middle(call: CallbackQuery):
    services = await search_groomer_for_middle_pet()
    await call.message.edit_reply_markup(reply_markup=list_of_groomer_services(services))


async def groomer_list_of_service_for_big(call: CallbackQuery):
    services = await search_groomer_for_big_pet()
    await call.message.edit_reply_markup(reply_markup=list_of_groomer_services(services))


async def back_to_weight_groomer_menu(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=weight_of_pet_menu_for_groomer())


def register_list_of_services_for_groomer(dp: Dispatcher):
    dp.register_callback_query_handler(groomer_list_of_service_for_mini, callback_weight_of_pet.filter(key='groomer_mini_weight'))
    dp.register_callback_query_handler(groomer_list_of_service_for_middle, callback_weight_of_pet.filter(key='groomer_middle_weight'))
    dp.register_callback_query_handler(groomer_list_of_service_for_big, callback_weight_of_pet.filter(key='groomer_big_weight'))
    dp.register_callback_query_handler(back_to_weight_groomer_menu, callback_weight_of_pet.filter(key='back_to_weight_for_groomer'))

