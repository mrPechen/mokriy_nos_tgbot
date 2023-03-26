from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from datetime import date, datetime, timedelta
from tgbot.keyboards.calendar_for_employees import employee_calendar_list, callback_employees_calendar
from tgbot.keyboards.inline import employees_category, callback_employees_category, callback_start_menu
from tgbot.services.db_commands import vet_groomer_category_filter


async def show_category(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=await employees_category())


async def show_employees_calendar(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=await employee_calendar_list())


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


async def employees_prev_month(call: CallbackQuery, callback_data: dict):
    temp_date = datetime(year=int(callback_data['year']), month=int(callback_data['month']), day=1)
    prev_date = temp_date - timedelta(days=1)
    await call.message.edit_reply_markup(reply_markup=await employee_calendar_list(year=int(prev_date.year),
                                                                                   month=int(prev_date.month)))


async def employees_next_month(call: CallbackQuery, callback_data: dict):
    year = int(callback_data['year'])
    month = int(callback_data['month'])
    next_year = year + 1 if month == 12 else year
    next_month = month % 12 + 1
    await call.message.edit_reply_markup(reply_markup=await employee_calendar_list(year=next_year,
                                                                                   month=next_month))


async def back_to_employees_category(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=await employees_category())


def register_employees_calendar(dp: Dispatcher):
    dp.register_callback_query_handler(show_category, callback_start_menu.filter(act='employees_calendar'))
    dp.register_callback_query_handler(show_employees_calendar, callback_employees_category.filter(act='get_empl_calendar'))
    dp.register_callback_query_handler(show_appointment_by_day, callback_employees_calendar.filter(act='day'))
    dp.register_callback_query_handler(employees_prev_month, callback_employees_calendar.filter(act='prev_month'))
    dp.register_callback_query_handler(back_to_employees_category, callback_employees_category.filter(act='back_to_category'))
    dp.register_callback_query_handler(employees_next_month, callback_employees_calendar.filter(act='next_month'))

