import asyncio
import schedule
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from parse_app.parse_func import get_page, parse_main_page, get_single_page, parse_single_page
from parse_app.db_func import add_or_update_article
from settings import API_TOKEN
from settings import URL, HEADERS
from bot.handlers import send_welcome, send_help, send_latest_article, search_article, handle_unknown_message

# TODO
from bot.handlers import send_latest_7_articles


# Инициализация бота с токеном
bot = Bot(token=API_TOKEN)

# Инициализация диспетчера для управления обработчиками
dp = Dispatcher(bot)

# Регистрация обработчиков команд
dp.register_message_handler(send_welcome, commands=['start'])
dp.register_message_handler(send_help, commands=['help'])
dp.register_message_handler(send_latest_article, commands=['latest'])
dp.register_message_handler(send_latest_7_articles, commands=['latest7'])
dp.register_message_handler(search_article, commands=['search'])
dp.register_message_handler(handle_unknown_message)


async def get_articles():
    # Получение основной страницы
    main_page_dict = await get_page(URL, HEADERS)
    main_page_text = main_page_dict['response']

    # Парсинг основной страницы и получение списка URL каждой новости
    url_list_single_pages = await parse_main_page(main_page_text)

    # Определение переменной с генератором (HTML страницы каждой новости)
    single_pages_dicts = await get_single_page(url_list_single_pages, HEADERS)

    for single_page_dict in single_pages_dicts:
        article_dict = parse_single_page(single_page_dict)
        await add_or_update_article(
            slug=article_dict['slug'],
            title=article_dict['title'],
            subtitle=article_dict['subtitle'],
            body=article_dict['body'],
            url_img=article_dict['url_img'],
            url_video=article_dict['url_video'],
            url_post=article_dict['url_post'],
            datetime_str=article_dict['datetime']
        )


async def schedule_jobs():
    # Запуск задачи каждый 20 секунд
    schedule.every(40).seconds.do(lambda: asyncio.create_task(get_articles()))
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher):
    # Запуск задачи обновления статей при старте
    asyncio.create_task(schedule_jobs())


def main():
    loop = asyncio.get_event_loop()
    # Запуск бота и обновление статей
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
