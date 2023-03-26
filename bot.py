import asyncio
import logging
import os
import django


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'admin.django_admin.settings'
)
os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': 'true'})
django.setup()


from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from tgbot.handlers.menu import register_start_menu
from tgbot.handlers.weight_of_pet import register_weight_menu
from tgbot.handlers.list_of_services import register_list_of_services
from tgbot.handlers.select_date import register_calendar
from tgbot.handlers.my_appointment import register_my_appointment
from tgbot.handlers.employees_handler import register_employees_calendar
from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.start import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware


logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_start_menu(dp)
    register_user(dp)
    register_weight_menu(dp)
    register_list_of_services(dp)
    register_calendar(dp)
    register_my_appointment(dp)
    register_employees_calendar(dp)


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)


    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
