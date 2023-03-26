from aiogram import Dispatcher, Bot
from aiogram.types import CallbackQuery
from datetime import date
from tgbot.keyboards.inline import action_with_appointments, callback_appointments, callback_start_menu, \
    button_list_for_cancel, callback_button_list_for_cancel
from tgbot.services.db_commands import show_my_appointments, cancel_appointments, get_service
from tgbot.config import load_config


async def my_appointments(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=action_with_appointments())


async def show_appointment(call: CallbackQuery):
    appointments = await show_my_appointments(user_id=call.from_user.id)
    await call.answer(cache_time=0)
    if appointments.count() == 0:
        await call.message.answer(text='Вы никуда не записаны.')
    else:
        text = ""
        num = 1
        for appointment in appointments:
            if appointment.date_of_reception >= date.today():
                text += f'{num}. Название: {appointment.service_id}\n' \
                        f'Цена: {appointment.service_id.price}\n' \
                        f'Дата: {appointment.date_of_reception}\n' \
                        f'Время: {appointment.time_of_reception[:-3]}\n' \
                        f'\n' \

                num += 1
        await call.message.answer(text='Ваши записи: \n\n' + text + 'Для возврата в главное меню нажмите /menu')


async def list_for_cancel_appointment(call: CallbackQuery):
    appointments = await show_my_appointments(user_id=call.from_user.id)
    await call.answer(cache_time=0)
    if appointments.count() == 0:
        await call.message.answer(text='Вы никуда не записаны.\n'
                                       '\n'
                                       'Для возврата в главное меню нажмите /menu')
    else:
        await call.message.answer(text='Выберете какую запись отменить.', reply_markup=await button_list_for_cancel(user_id=call.from_user.id))


async def cancel_appointment(call: CallbackQuery, callback_data: dict):
    user_id = call.from_user.id
    service_id = callback_data['service']
    dates = callback_data['date']
    times = callback_data['time']
    service = await get_service(service_id)
    config = load_config('.env').tg_bot
    bot = Bot(token=config.token)
    await cancel_appointments(user_id, int(service_id), dates, times.replace('-', ':'))
    await call.answer(cache_time=0)
    await call.message.answer(text=f'Запись на услугу "{service.name}" отменена\n'
                                   f'\n'
                                   f'Для возврата в главное меню нажмите /menu')
    for admin in config.admin_ids:
        session = await Bot.get_session(bot)
        await Bot.send_message(bot, chat_id=admin, text=f"\u274C ОТМЕНА ЗАПИСИ!\n"
                                                        f"Клиент: {call.from_user.full_name}\n"
                                                        f"Услуга: {service.name}\n"
                                                        f"Дата: {dates}\n"
                                                        f"Время: {times[:-3]}")
        await session.close()


async def back_to_my_appointments(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=action_with_appointments())


def register_my_appointment(dp: Dispatcher):
    dp.register_callback_query_handler(my_appointments, callback_start_menu.filter(act='appointment'))
    dp.register_callback_query_handler(show_appointment, callback_appointments.filter(act='show_appointments'))
    dp.register_callback_query_handler(list_for_cancel_appointment, callback_appointments.filter(act='cancel_appointments'))
    dp.register_callback_query_handler(cancel_appointment, callback_button_list_for_cancel.filter(act='delete'))
    dp.register_callback_query_handler(back_to_my_appointments, callback_appointments.filter(act='back_to_appointments'))


