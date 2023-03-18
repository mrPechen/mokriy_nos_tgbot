from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton, ContentTypes
from datetime import date, time, datetime, timedelta
from tgbot.keyboards.psycho_calendar import psycho_calendar_list, psycho_time_list, psycho_calendar_callback
from tgbot.keyboards.reply import callback_start_menu
from tgbot.services.db_commands import save_phone_number, get_phone_number, save_psycho_registration


async def get_psycho_calendar(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=await psycho_calendar_list())


async def show_time_list(call: CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup(reply_markup=await psycho_time_list(year=int(callback_data['year']),
                                                                             month=int(callback_data['month']),
                                                                             day=int(callback_data['day'])))


async def psycho_prev_month(call: CallbackQuery, callback_data: dict):
    temp_date = datetime(year=int(callback_data['year']), month=int(callback_data['month']), day=1)
    prev_date = temp_date - timedelta(days=1)
    await call.message.edit_reply_markup(reply_markup=await psycho_calendar_list(year=int(prev_date.year),
                                                                                 month=int(prev_date.month)))


async def psycho_next_month(call: CallbackQuery, callback_data: dict):
    temp_date = datetime(year=int(callback_data['year']), month=int(callback_data['month']), day=1)
    next_date = temp_date + timedelta(days=31)
    await call.message.edit_reply_markup(reply_markup=await psycho_calendar_list(year=int(next_date.year),
                                                                                 month=int(next_date.month)))


async def psycho_save_number(mess=Message):
    contact = mess.contact.phone_number
    if await get_phone_number(user_id=mess.from_user.id) is None:
        await save_phone_number(user_id=mess.from_user.id, phone_number=contact)
        await mess.answer(text=f'Ваш номер: {contact} получен! Выберете, пожалуйста, время в меню выше еще раз.')
    else:
        pass


async def registration_psycho(call: CallbackQuery, callback_data: dict):
    if await get_phone_number(user_id=call.from_user.id) is None:
        await call.message.answer(text='Для записи нам нужен ваш номер. Нажмите на кнопку ниже, чтобы прислать его.\n'
                                       'При повторной записи ваш номер уже не потребуется.',
                                  reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).insert(
                                    KeyboardButton(text='Отправить номер телефона', request_contact=True)))
        await call.answer(show_alert=False, cache_time=2)

    else:
        await save_psycho_registration(user_id=call.from_user.id,
                                       date_of_reception=date(year=int(callback_data['year']),
                                                              month=int(callback_data['month']),
                                                              day=int(callback_data['day'])),
                                       time_of_reception=time(hour=int(callback_data["hour"]),
                                                              minute=int(callback_data["minutes"])))
        await call.message.answer(text=f"Вы записаны к зоопсихологу.\n"
                                       f"Цена: "
                                       f"Дата: {date(year=int(callback_data['year']),month=int(callback_data['month']),day=int(callback_data['day']))}\n"
                                       f"Время: {time(hour=int(callback_data['hour']),minute=int(callback_data['minutes']))}\n"
                                       f"\n"
                                       f"Для возврата в главное меню нажмите /menu")


async def back_to_calendar(call: CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup(reply_markup=await psycho_calendar_list(month=int(callback_data['month'])))


def register_psycho_handler(dp: Dispatcher):
    dp.register_callback_query_handler(get_psycho_calendar, callback_start_menu.filter(key='zoopsych'))
    dp.register_callback_query_handler(show_time_list, psycho_calendar_callback.filter(act='DAY'))
    dp.register_callback_query_handler(psycho_prev_month, psycho_calendar_callback.filter(act='PREV-MONTH'))
    dp.register_callback_query_handler(psycho_next_month, psycho_calendar_callback.filter(act='NEXT-MONTH'))
    dp.register_message_handler(psycho_save_number, content_types=ContentTypes.CONTACT)
    dp.register_callback_query_handler(registration_psycho, psycho_calendar_callback.filter(act='TIME'))
    dp.register_callback_query_handler(back_to_calendar, psycho_calendar_callback.filter(act='Back_to_psycho_calendar'))
