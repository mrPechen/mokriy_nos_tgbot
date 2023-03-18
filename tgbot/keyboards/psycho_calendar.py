import calendar
from datetime import datetime, date
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from tgbot.services.db_commands import psycho_category_filter, count_psycho_time
from pytz import timezone

psycho_calendar_callback = CallbackData('calendar_callback', 'act', 'year', 'month', 'day', 'hour', 'minutes')


async def psycho_calendar_list(year: int = datetime.now().year, month: int = datetime.now().month):
    ignore_callback = psycho_calendar_callback.new("IGNORE", year, month, 0, 0, 0)
    markup = InlineKeyboardMarkup(row_width=7)
    markup.row()
    markup.insert(
        InlineKeyboardButton(
            text=f'{calendar.month_name[month]} {str(year)}',
            callback_data=ignore_callback
        )
    )
    markup.row()
    for day in ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']:
        markup.insert(
            InlineKeyboardButton(
                text=day,
                callback_data=ignore_callback
            )
        )
    month_calendar = calendar.monthcalendar(year=year, month=month)
    for week in month_calendar:
        markup.row()
        for day in week:
            date_2 = date(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
            utc = timezone('Europe/Moscow')
            curr_time = datetime(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
                                 hour=datetime.now().hour, minute=datetime.now().minute).astimezone(utc)
            if day == 0 or await count_psycho_time(date=date(int(year), int(month), int(day))) >= 18:
                markup.insert(
                    InlineKeyboardButton(
                        text=' ',
                        callback_data=ignore_callback
                    )
                )
                continue
            if day > 0 and date(year=year, month=month, day=int(day)) < date_2 or str(curr_time.time()) >= '20:30':
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
                    callback_data=psycho_calendar_callback.new("DAY", year, month, day, 0, 0)
                )
            )

    markup.row()
    if month == datetime.now().month:
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
                callback_data=psycho_calendar_callback.new("PREV-MONTH", year, month, day, 0, 0)
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text=' ',
            callback_data=ignore_callback
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text='>',
            callback_data=psycho_calendar_callback.new("NEXT-MONTH", year, month, day, 0, 0)
        )
    )
    return markup


async def psycho_time_list(year: int, month: int, day: int):
    ignore_callback = psycho_calendar_callback.new("IGNORE", year, month, 0, 0, 0)
    markup = InlineKeyboardMarkup(row_width=3)
    times = ['12-00', '12-30', '13-00', '13-30', '14-00', '14-30', '15-00', '15-30',
             '16-00', '16-30', '17-00', '17-30', '18-00', '18-30', '19-00', '19-30',
             '20-00', '20-30']
    time_check = await psycho_category_filter(date=date(int(year), int(month), int(day)))
    unavailable_time = [i.time_of_reception.replace(':', '-')[:-3] for i in time_check]
    utc = timezone('Europe/Moscow')
    curr_time = datetime(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, hour=datetime.now().hour, minute=datetime.now().minute).astimezone(utc)
    if time_check:
        for time in times:
            if time in unavailable_time:
                markup.insert(
                    InlineKeyboardButton(
                        text=' ',
                        callback_data=ignore_callback
                    )
                )
                continue
            if time <= f'{curr_time.hour}-{curr_time.minute}' and str(date(year, month, day)) == str(date(curr_time.year, curr_time.month, curr_time.day)):
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
                    callback_data=psycho_calendar_callback.new("TIME", year, month, day, time.split('-')[0],
                                                        time.split('-')[1]),
                )
            )
        markup.insert(
            InlineKeyboardButton(
                text='Назад',
                callback_data=psycho_calendar_callback.new("Back_to_psycho_calendar", year, month, day, 0, 0)
            )
        )
    else:
        for time in times:
            if time <= f'{curr_time.hour}-{curr_time.minute}' and str(date(year, month, day)) == str(date(curr_time.year, curr_time.month, curr_time.day)):
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
                    callback_data=psycho_calendar_callback.new("TIME", year, month, day, time.split('-')[0], time.split('-')[1]),
                )
            )
        markup.insert(
            InlineKeyboardButton(
                text='Назад',
                callback_data=psycho_calendar_callback.new("Back_to_psycho_calendar", year, month, day, 0, 0)
            )
        )
    return markup
