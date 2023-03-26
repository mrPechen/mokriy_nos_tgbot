from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from tgbot.keyboards.inline import services_list, callback_weight_of_pet, callback_show_service, \
    show_full_service_info_menu
from tgbot.services.db_commands import get_service


async def services_menu(call: CallbackQuery, callback_data: dict):
    weight_id = callback_data['weight_id']
    category = callback_data['category']
    await call.message.edit_reply_markup(reply_markup=await services_list(weight_id, category))


async def show_full_info(call: CallbackQuery, callback_data: dict):
    category = callback_data['category']
    weight_id = callback_data['weight_id']
    service_id = callback_data['service_id']
    service_info = await get_service(service_id)
    if service_info.description == '':
        await call.message.answer(text=f'Название услуги: {service_info.name}\n'
                                       f'Цена: {service_info.price}\n',
                                  reply_markup=show_full_service_info_menu(category, weight_id, service_id))
    else:
        await call.message.answer(text=f'Название: {service_info.name}\n'
                                       f'Цена: {service_info.price}\n'
                                       f'Описание: {service_info.description}',
                                  reply_markup=show_full_service_info_menu(category, weight_id, service_id))


async def back_to_services_menu(call: CallbackQuery, callback_data: dict):
    weight_id = callback_data['weight_id']
    category = callback_data['category']
    await call.message.edit_reply_markup(reply_markup=await services_list(weight_id, category))


def register_list_of_services(dp: Dispatcher):
    dp.register_callback_query_handler(services_menu, callback_weight_of_pet.filter(act='pet_weight'))
    dp.register_callback_query_handler(show_full_info, callback_show_service.filter(act='show_full_info'))
    dp.register_callback_query_handler(back_to_services_menu, callback_show_service.filter(act='back_to_services'))
