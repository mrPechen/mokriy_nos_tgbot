from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from datetime import date
from tgbot.services.db_commands import show_my_appointments, get_category, get_weight, search_services_by_weight

callback_start_menu = CallbackData('callback_start_menu', 'act', 'category_id')
callback_show_service = CallbackData('callback_show_service', 'act', 'category', 'weight_id', 'service_id')
callback_appointments = CallbackData('callback_appointments', 'act')
callback_button_list_for_cancel = CallbackData('callback_button_list_for_cancel', 'act', 'service', 'date', 'time')
callback_employees_category = CallbackData('callback_employees_category', 'act')
callback_weight_of_pet = CallbackData('callback_weight_of_pet', 'act', 'category', 'weight_id')
callback_full_info = CallbackData('callback_full_info', 'act', 'category', 'weight_id', 'service_id')

async def menu_user():
    markup = InlineKeyboardMarkup(row_width=1)
    categories = await get_category()
    for category in categories:
        markup.insert(
            InlineKeyboardButton(
                text=f'{category.name}',
                callback_data=callback_start_menu.new(act='category', category_id=f'{category.id}')
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text='Мои записи \U0001F5D3',
            callback_data=callback_start_menu.new(act='appointment', category_id=0)
        )
    )
    return markup


async def menu_admin():
    markup = InlineKeyboardMarkup(row_width=2)
    categories = await get_category()
    for category in categories:
        markup.insert(
            InlineKeyboardButton(
                text=f'{category.name}',
                callback_data=callback_start_menu.new(act='category', category_id=f'{category.id}')
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text='Админка', url="http://0.0.0.0:8000/admin",
            callback_data=callback_start_menu.new(act='admin', category_id=0)
        )
    ),
    markup.insert(
        InlineKeyboardButton(
            text='Мои записи \U0001F5D3',
            callback_data=callback_start_menu.new(act='appointment', category_id=0)
        )
    ),
    markup.insert(
        InlineKeyboardButton(
            text='Календарь работника',
            callback_data=callback_start_menu.new(act='employees_calendar', category_id=0)
        )
    )
    return markup


async def pet_weight(category):
    markup = InlineKeyboardMarkup(row_width=1)
    weight_list = await get_weight()
    for weight in weight_list:
        markup.insert(
            InlineKeyboardButton(
                text=f'{weight.name}',
                callback_data=callback_weight_of_pet.new(act='pet_weight', category=category, weight_id=f'{weight.id}')
            )
        )
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=callback_start_menu.new(act='back_to_menu', category_id=category)
        )
    )
    return markup


async def services_list(weight_id, category):
    markup = InlineKeyboardMarkup(row_width=1)
    services = await search_services_by_weight(weight_id=weight_id, category=category)
    for service in services:
        markup.insert(
            InlineKeyboardButton(
                text=f'{service.name}\n',
                callback_data=callback_show_service.new(act='show_full_info', category=category, weight_id=weight_id, service_id=service.id)
            )
        ),
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=callback_weight_of_pet.new(act='back_to_weight', category=category, weight_id=weight_id)
        )
    )
    return markup


def action_with_appointments():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(
        InlineKeyboardButton(
            text='Показать записи',
            callback_data=callback_appointments.new(act='show_appointments')
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text='Отменить запись',
            callback_data=callback_appointments.new(act='cancel_appointments')
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text='Назад',
            callback_data=callback_start_menu.new(act='back_to_menu', category_id=0)
        )
    )
    return markup


async def button_list_for_cancel(user_id):
    appointments = await show_my_appointments(user_id=user_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for appointment in appointments:
        if appointment.date_of_reception >= date.today():
            markup.insert(
                InlineKeyboardButton(
                    text=f'{appointment.service_id}\n'
                         f'{appointment.date_of_reception}',
                    callback_data=callback_button_list_for_cancel.new(act='delete', service=appointment.service_id.id, date=appointment.date_of_reception, time=appointment.time_of_reception.replace(':', '-'))
                )
            )
            continue
    markup.insert(
        InlineKeyboardButton(
            text='Назад',
            callback_data=callback_appointments.new(act='back_to_appointments')
        )
    )
    return markup


async def employees_category():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(
            InlineKeyboardButton(
                text=f'Ветврач/Косметолог',
                callback_data=callback_employees_category.new(act='get_empl_calendar')
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text='Назад',
            callback_data=callback_start_menu.new(act='back_to_menu', category_id=0)
        )
    )
    return markup


def show_full_service_info_menu(category, weight_id, service_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(
        InlineKeyboardButton(
            text='Записаться',
            callback_data=callback_full_info.new(act='calendar', category=category, weight_id=weight_id, service_id=service_id)
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text='Назад',
            callback_data=callback_show_service.new(act='back_to_services', category=category, weight_id=weight_id, service_id=service_id)
        )
    )
    return markup