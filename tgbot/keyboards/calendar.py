import calendar
from datetime import datetime, date, timezone, time as tm, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from tgbot.keyboards.inline import callback_show_service
from tgbot.services.db_commands import vet_groomer_category_filter, count_by_dates, get_employee
from pytz import timezone

calendar_callback = CallbackData('calendar_callback', 'act', 'year', 'month', 'day', 'hour', 'minutes', 'category', 'weight_id', 'service_id')


async def calendar_list(year: int = datetime.now().year, month: int = datetime.now().month, category=None, weight_id=None,  service_id: int = None):
    ignore_callback = calendar_callback.new("ignore", year, month, 0, 0, 0, 0, 0, 0)
    markup = InlineKeyboardMarkup(row_width=7)
    markup.row()
    markup.insert(
        InlineKeyboardButton(
            text=f'{calendar.month_name[month]} {str(year)}',
            callback_data=ignore_callback
        )
    )
    markup.row()
    for day in ['Ср', 'Чт', 'Пт', 'Сб', 'Вс']:
        markup.insert(
            InlineKeyboardButton(
                text=day,
                callback_data=ignore_callback
            )
        )
    month_calendar = calendar.monthcalendar(year=year, month=month)
    get_employee_data = await get_employee()
    start_vacation = get_employee_data.vacation_date_start
    end_vacation = get_employee_data.vacation_date_end
    vacation = None
    if start_vacation and end_vacation:
        vacation = [start_vacation+timedelta(days=x) for x in range((end_vacation-start_vacation).days)]
    max_appointments = 32
    get_count_data = await count_by_dates(year, month)
    days_with_max_appointments = [i['date_of_reception__day'] for i in get_count_data if i['count'] >= max_appointments]
    today = date.today()
    utc = timezone('Europe/Moscow')
    curr_time = datetime.now().astimezone(utc)
    for week in month_calendar:
        markup.row()
        for day in week[2:]:
            if day == 0 or day in days_with_max_appointments:
                markup.insert(
                    InlineKeyboardButton(
                        text=' ',
                        callback_data=ignore_callback
                    )
                )
                continue
            elif day > 0 and date(year=year, month=month, day=int(day)) < today:
                markup.insert(
                    InlineKeyboardButton(
                        text=' ',
                        callback_data=ignore_callback
                    )
                )
                continue
            elif vacation and day > 0 and date(year=year, month=month, day=int(day)) in vacation:
                markup.insert(
                    InlineKeyboardButton(
                        text=' ',
                        callback_data=ignore_callback
                    )
                )
                continue
            elif curr_time.time() >= tm(hour=20, minute=30) and date(year=year, month=month, day=int(day)) <= today:
                markup.insert(
                    InlineKeyboardButton(
                        text=' ',
                        callback_data=ignore_callback
                    )
                )
                continue
            markup.insert(
                InlineKeyboardButton(
                    text=str(day),
                    callback_data=calendar_callback.new("day", year, month, day, 0, 0, category, weight_id, service_id)
                )
            )

    markup.row()
    if month == datetime.now().month and year == datetime.now().year:
        markup.insert(
            InlineKeyboardButton(
                text=' ',
                callback_data=ignore_callback
            )
        )
    else:
        markup.insert(
            InlineKeyboardButton(
                text='<',
                callback_data=calendar_callback.new("prev_month", year, month, day, 0, 0, category, weight_id, service_id)
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text='Назад',
            callback_data=callback_show_service.new(act='back_to_services', category=category, weight_id=weight_id, service_id=service_id)
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text='>',
            callback_data=calendar_callback.new("next_month", year, month, day, 0, 0, category, weight_id, service_id)
        )
    )
    return markup


async def time_list(year: int, month: int, day: int, category, weight_id, service_id: int):
    ignore_callback = calendar_callback.new("ignore", year, month, 0, 0, 0, 0, 0, 0)
    markup = InlineKeyboardMarkup(row_width=3)
    time_list = [f'{h}-{m}' for h in range(12, 21) for m in ['00', '15', '30', '45']]
    get_employee_data = await get_employee()
    break_time_start = get_employee_data.break_time_start.hour
    break_time_end = get_employee_data.break_time_end.hour
    break_times = [f'{h}-{m}' for h in range(break_time_start, break_time_end) for m in ['00', '15', '30', '45']]
    time_check = await vet_groomer_category_filter(date=date(int(year), int(month), int(day)))
    unavailable_time = [i.time_of_reception.replace(':', '-')[:-3] for i in time_check]
    utc = timezone('Europe/Moscow')
    curr_time = datetime.now().astimezone(utc)
    selected_date = date(year, month, day)
    for time in time_list:
        if time_check:
            if time in unavailable_time:
                markup.insert(
                    InlineKeyboardButton(
                        text=' ',
                        callback_data=ignore_callback
                    )
                )
                continue
            elif time in break_times:
                markup.insert(
                    InlineKeyboardButton(
                        text=' ',
                        callback_data=ignore_callback
                    )
                )
                continue
            elif tm(hour=int(time.split('-')[0]), minute=int(time.split('-')[1])) <= curr_time.time() and selected_date == date.today():
                markup.insert(
                    InlineKeyboardButton(
                        text=' ',
                        callback_data=ignore_callback
                    )
                )
                continue
            markup.insert(
                InlineKeyboardButton(
                    text=time,
                    callback_data=calendar_callback.new("time", year, month, day, time.split('-')[0],
                                                        time.split('-')[1], category, weight_id, service_id),
                )
            )
        if not time_check:
            if tm(hour=int(time.split('-')[0]), minute=int(time.split('-')[1])) <= curr_time.time() and selected_date == date.today():
                markup.insert(
                    InlineKeyboardButton(
                        text=' ',
                        callback_data=ignore_callback
                    )
                )
                continue
            elif time in break_times:
                markup.insert(
                    InlineKeyboardButton(
                        text=' ',
                        callback_data=ignore_callback
                    )
                )
                continue
            markup.insert(
                InlineKeyboardButton(
                    text=time,
                    callback_data=calendar_callback.new("time", year, month, day, time.split('-')[0], time.split('-')[1],
                                                        category, weight_id, service_id),
                )
            )
    markup.insert(
            InlineKeyboardButton(
                text='Назад',
                callback_data=calendar_callback.new("Back_to_calendar", year, month, day, 0, 0, category, weight_id, service_id)
            )
        )
    return markup
