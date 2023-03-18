from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from datetime import date
from tgbot.services.db_commands import show_my_appointments, get_category

callback_start_menu = CallbackData('callback_start_menu', 'key')
callback_weight_of_pet = CallbackData('callback_weight_of_pet', 'key')
callback_show_service = CallbackData('callback_show_service', 'key', 'service_id')
callback_appointments = CallbackData('callback_appointments', 'key')
callback_button_list_for_cancel = CallbackData('callback_button_list_for_cancel', 'act', 'service', 'date', 'time')
callback_employer_category = CallbackData('callback_employer_category', 'act')


def menu_user():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(
        InlineKeyboardButton(
            text='Вет. услуги \U0001F469\u200D\u2695\uFE0F',
            callback_data=callback_start_menu.new(key='vetdoc')
        )
    ),
    """markup.insert(
        InlineKeyboardButton(
            text='Зоопсихолог \U0001F49C',
            callback_data=callback_start_menu.new(key='zoopsych')

        )
    ),"""
    markup.insert(
        InlineKeyboardButton(
            text='Услуги красоты \U0001F436',
            callback_data=callback_start_menu.new(key='groomer')
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text='Мои записи',
            callback_data=callback_start_menu.new(key='appointment')
        )
    ),
    return markup


def menu_admin():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(
        InlineKeyboardButton(
            text='Вет. услуги \U0001F469\u200D\u2695\uFE0F',
            callback_data=callback_start_menu.new(key='vetdoc')
        )
    ),
    """markup.insert(
        InlineKeyboardButton(
            text='Зоопсихолог \U0001F49C',
            callback_data=callback_start_menu.new(key='zoopsych')

        )
    ),"""
    markup.insert(
        InlineKeyboardButton(
            text='Услуги красоты \U0001F436',
            callback_data=callback_start_menu.new(key='groomer')
        )
    ),
    markup.insert(
        InlineKeyboardButton(
            text='Админка', url="http://0.0.0.0:8000/admin",
            callback_data=callback_start_menu.new(key='admin')
        )
    ),
    markup.insert(
        InlineKeyboardButton(
            text='Мои записи',
            callback_data=callback_start_menu.new(key='appointment')
        )
    ),
    markup.insert(
        InlineKeyboardButton(
            text='Календарь работника',
            callback_data=callback_start_menu.new(key='employer_calendar')
        )
    )
    return markup


def weight_of_pet_menu_for_vet():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(
        InlineKeyboardButton(
            text='Маленькие породы (вес до 5 кг.)',
            callback_data=callback_weight_of_pet.new(key='vet_mini_weight')

        )
    ),
    markup.insert(
        InlineKeyboardButton(
            text='Средние породы (вес от 5 кг. до 15 кг.)',
            callback_data=callback_weight_of_pet.new(key='vet_middle_weight')

        )
    ),
    markup.insert(
        InlineKeyboardButton(
            text='Большиие породы (вес от 15 кг.)',
            callback_data=callback_weight_of_pet.new(key='vet_big_weight')
        )
    ),
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=callback_start_menu.new(key='back_to_menu')
        )
    )
    return markup


def weight_of_pet_menu_for_groomer():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(
        InlineKeyboardButton(
            text='Маленькие породы (вес до 5 кг.)',
            callback_data=callback_weight_of_pet.new(key='groomer_mini_weight')

        )
    ),
    markup.insert(
        InlineKeyboardButton(
            text='Средние породы (вес от 5 кг. до 15 кг.)',
            callback_data=callback_weight_of_pet.new(key='groomer_middle_weight')

        )
    ),
    markup.insert(
        InlineKeyboardButton(
            text='Большиие породы (вес от 15 кг.)',
            callback_data=callback_weight_of_pet.new(key='groomer_big_weight')
        )
    ),
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=callback_start_menu.new(key='back_to_menu')
        )
    )
    return markup


def list_of_vet_services(services):
    markup = InlineKeyboardMarkup(row_width=2)
    for service in services:
        markup.insert(
            InlineKeyboardButton(
                text=f'{service.name}',
                callback_data=callback_show_service.new(key='calendar', service_id=f'{service.id}')
            )
        ),
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=callback_weight_of_pet.new(key='back_to_weight_for_vet')
        )
    )
    return markup


def list_of_groomer_services(services):
    markup = InlineKeyboardMarkup(row_width=2)
    for service in services:
        markup.insert(
            InlineKeyboardButton(
                text=f'{service.name}',
                callback_data=callback_show_service.new(key='calendar', service_id=f'{service.id}')
            )
        ),
    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=callback_weight_of_pet.new(key='back_to_weight_for_groomer')
        )
    )
    return markup


def action_with_appointments():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(
        InlineKeyboardButton(
            text='Показать записи',
            callback_data=callback_appointments.new(key='show_appointments')
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text='Отменить запись',
            callback_data=callback_appointments.new(key='cancel_appointments')
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text='Назад',
            callback_data=callback_start_menu.new(key='back_to_menu')
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
            callback_data=callback_appointments.new(key='back_to_appointments')
        )
    )
    return markup


async def employer_category():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(
            InlineKeyboardButton(
                text=f'Ветврач/Косметолог',
                callback_data=callback_employer_category.new(act='get_empl_calendar')
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text='Назад',
            callback_data=callback_start_menu.new(key='back_to_menu')
        )
    )
    return markup
