from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from datetime import date
from tgbot.keyboards.calendar_for_employer import employer_calendar_list, callback_employer_calendar
from tgbot.keyboards.reply import employer_category, callback_employer_category, callback_start_menu
from tgbot.services.db_commands import vet_groomer_category_filter


async def show_category(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=await employer_category())


async def show_employer_calendar(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=await employer_calendar_list())


async def show_appointment_by_day(call: CallbackQuery, callback_data: dict):
    data = date(year=int(callback_data['year']), month=int(callback_data['month']), day=int(callback_data['day']))
    appointments = await vet_groomer_category_filter(date=data)
    text = ""
    num = 1
    for appointment in appointments:
        text += f'{num}. Название: {appointment.service_id}\n' \
                f'Имя: {appointment.registrated.name}\n' \
                f'Аккаунт телеграм: @{appointment.registrated.username}\n' \
                f'Дата: {appointment.date_of_reception}\n' \
                f'Время: {appointment.time_of_reception[:-3]}\n' \
                f'Телефон: {appointment.phone_number}\n' \
                f'\n'
        num += 1
    await call.message.answer(text=text + 'Для возврата в главное меню нажмите /menu')
    await call.answer(cache_time=0)


async def back_to_employers_category(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=await employer_category())


def register_employer_calendar(dp: Dispatcher):
    dp.register_callback_query_handler(show_category, callback_start_menu.filter(act='employer_calendar'))
    dp.register_callback_query_handler(show_employer_calendar, callback_employer_category.filter(act='get_empl_calendar'))
    dp.register_callback_query_handler(show_appointment_by_day, callback_employer_calendar.filter(act='DAY'))
    dp.register_callback_query_handler(back_to_employers_category, callback_employer_category.filter(act='back_to_category'))
