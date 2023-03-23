import calendar
from datetime import datetime, date

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.reply import callback_employer_category
from tgbot.services.db_commands import vet_groomer_category_count

callback_employer_calendar = CallbackData('callback_employer_calendar', 'act', 'year', 'month', 'day')


async def employee_calendar_list(year: int = datetime.now().year, month: int = datetime.now().month):
    ignore_callback = callback_employer_calendar.new("IGNORE", year, month, 0)
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
            if day == 0:
                markup.insert(
                    InlineKeyboardButton(
                        text=' ',
                        callback_data=ignore_callback
                    )
                )
                continue
            if day > 0 and await vet_groomer_category_count(date=date(year, month, day)) == 0:
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
                    callback_data=callback_employer_calendar.new("DAY", year, month, day)
                )
            )
    markup.insert(
        InlineKeyboardButton(
            text='Назад',
            callback_data=callback_employer_category.new(act='back_to_category')
        )
    )
    return markup



