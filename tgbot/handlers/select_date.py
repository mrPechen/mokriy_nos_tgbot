from aiogram import Dispatcher, Bot
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ContentTypes, Message
from datetime import datetime, timedelta, time, date
from tgbot.config import load_config
from tgbot.keyboards.calendar import calendar_list, calendar_callback, time_list
from tgbot.keyboards.inline import callback_full_info
from tgbot.services.db_commands import save_registration, get_phone_number, save_phone_number, get_service


async def select_date_vet(call: CallbackQuery, callback_data: dict):
    category = callback_data['category']
    weight_id = callback_data['weight_id']
    service_id = int(callback_data['service_id'])
    await call.message.edit_reply_markup(reply_markup=await calendar_list(category=category,
                                                                          weight_id=weight_id,
                                                                          service_id=service_id))


async def prev_month(call: CallbackQuery, callback_data: dict):
    category = callback_data['category']
    weight_id = callback_data['weight_id']
    service_id = int(callback_data['service_id'])
    temp_date = datetime(year=int(callback_data['year']), month=int(callback_data['month']), day=1)
    prev_date = temp_date - timedelta(days=1)
    await call.message.edit_reply_markup(reply_markup=await calendar_list(year=int(prev_date.year),
                                                                          month=int(prev_date.month),
                                                                          category=category,
                                                                          weight_id=weight_id,
                                                                          service_id=service_id))


async def next_month(call: CallbackQuery, callback_data: dict):
    year = int(callback_data['year'])
    month = int(callback_data['month'])
    category = callback_data['category']
    weight_id = callback_data['weight_id']
    service_id = int(callback_data['service_id'])
    next_year = year + 1 if month == 12 else year
    next_month = month % 12 + 1
    await call.message.edit_reply_markup(reply_markup=await calendar_list(year=next_year,
                                                                          month=next_month,
                                                                          category=category,
                                                                          weight_id=weight_id,
                                                                          service_id=service_id))


async def select_day(call: CallbackQuery, callback_data: dict):
    category = callback_data['category']
    weight_id = callback_data['weight_id']
    service_id = int(callback_data['service_id'])
    await call.message.edit_reply_markup(reply_markup=await time_list(year=int(callback_data['year']),
                                                                      month=int(callback_data['month']),
                                                                      day=int(callback_data['day']),
                                                                      category=category,
                                                                      weight_id=weight_id,
                                                                      service_id=service_id))


async def back_to_calendar(call: CallbackQuery, callback_data: dict):
    category = callback_data['category']
    weight_id = callback_data['weight_id']
    service_id = int(callback_data['service_id'])
    await call.message.edit_reply_markup(reply_markup=await calendar_list(month=int(callback_data['month']),
                                                                          category=category,
                                                                          weight_id=weight_id,
                                                                          service_id=service_id
                                                                          ))


async def save_number(mess=Message):
    contact = mess.contact.phone_number
    if await get_phone_number(user_id=mess.from_user.id) is None:
        await save_phone_number(user_id=mess.from_user.id, phone_number=contact)
        await mess.answer(text=f'Ваш номер: {contact} получен! Выберете, пожалуйста, время в меню выше еще раз.')
    else:
        pass


async def registration(call: CallbackQuery, callback_data: dict):
    if await get_phone_number(user_id=call.from_user.id) is None:
        await call.message.answer(text='Для записи нам нужен ваш номер. Нажмите на кнопку ниже, чтобы прислать его.\n'
                                       'При повторной записи ваш номер уже не потребуется.',
                                  reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).insert(
                                    KeyboardButton(text='Отправить номер телефона', request_contact=True)))
    else:
        config = load_config('.env').tg_bot
        bot = Bot(token=config.token)
        service = await get_service(service_id=int(callback_data['service_id']))
        phone = await get_phone_number(user_id=call.from_user.id)

        await save_registration(user_id=call.from_user.id, service_id=int(callback_data['service_id']),
                                date_of_reception=date(year=int(callback_data['year']),
                                                       month=int(callback_data['month']),
                                                       day=int(callback_data['day'])),
                                time_of_reception=time(hour=int(callback_data["hour"]),
                                                       minute=int(callback_data["minutes"])))
        await call.message.answer(text=f"Вы записаны на улсугу: {service.name}\n"
                                       f"Сумма: {service.price}\n"
                                       f"Дата: {date(year=int(callback_data['year']),month=int(callback_data['month']),day=int(callback_data['day']))}\n"
                                       f"Время: {callback_data['hour']}:{callback_data['minutes']}\n"
                                       f"\n"
                                       f"Скоро увидимся! \U0001F43E \u2764 \n"
                                       f"\n"
                                       f"Для возврата в главное меню нажмите /menu")
        for admin in config.admin_ids:
            session = await Bot.get_session(bot)
            await Bot.send_message(bot, chat_id=admin, text=f'\u2705 НОВАЯ ЗАПИСЬ!\n'
                                                            f'Имя: {call.from_user.full_name}\n'
                                                            f'Название услуги: {service.name}\n'
                                                            f'Дата: {date(year=int(callback_data["year"]),month=int(callback_data["month"]),day=int(callback_data["day"]))}\n'
                                                            f'Время: {callback_data["hour"]}:{callback_data["minutes"]}\n'
                                                            f'Номер телефона: {phone}')
            await session.close()

    await call.answer(cache_time=0)


def register_calendar(dp: Dispatcher):
    dp.register_callback_query_handler(select_date_vet, callback_full_info.filter(act='calendar'))
    dp.register_callback_query_handler(prev_month, calendar_callback.filter(act='prev_month'))
    dp.register_callback_query_handler(next_month, calendar_callback.filter(act='next_month'))
    dp.register_callback_query_handler(select_day, calendar_callback.filter(act='day'))
    dp.register_message_handler(save_number, content_types=ContentTypes.CONTACT)
    dp.register_callback_query_handler(registration, calendar_callback.filter(act='time'))
    dp.register_callback_query_handler(back_to_calendar, calendar_callback.filter(act='Back_to_calendar'))



