import asyncio

from aiogram import types
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from parse_app.db_func import get_latest_article
from parse_app.db_func import search_articles_by_keyword
from parse_app.db_func import get_latest_7_articles

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('/help'))
keyboard.add(KeyboardButton('/latest'))
keyboard.add(KeyboardButton('/latest7'))


async def send_welcome(message: types.Message):
    """
    Обработчик команды /start.
    Args: message (types.Message): Объект сообщения.
    """
    await message.reply("Добро пожаловать!👋 Используйте кнопки ниже, чтобы получать последние новости или"
                        " вызвать список доступных команд.",
                        reply_markup=keyboard)


async def send_help(message: types.Message):
    help_text = (
        "📜 *Список доступных команд:*\n\n"
        "/start - Начать работу с ботом и получить приветственное сообщение\n"
        "/latest - Получить последнюю новость\n"
        "/latest - Получить 7 последних новостей\n"
        "/search <ключевое слово> - Искать статьи по ключевому слову в заголовках\n"
        "Но знай что лингвистический анализ текста, это сложно и пока придется искать без учета падежей😔\n"
        "/help - Показать это сообщение помощи\n"
    )
    await message.reply(help_text, parse_mode=ParseMode.MARKDOWN)


async def send_latest_article(message: types.Message):
    """
    Обработчик команды /latest. Отправляет последнюю статью из базы данных.
    Args: message (types.Message): Объект сообщения.
    """
    article = get_latest_article()

    if article:
        # Распаковка данных статьи
        slug, title, subtitle, body, url_img, url_video, url_post, datetime = article

        # Формирование ответа, начиная с заголовка
        response = f"*{title}*\n\n"

        # Добавление подзаголовка, если он не пустой
        if subtitle:
            response += f"{subtitle}\n\n"
        # Добавление основного текста статьи, если он не пустой
        if body:
            response += f"{body}\n\n"
        # Добавление ссылки на изображение, если она не пустая
        if url_img:
            response += f"[Image]({url_img})\n"
        # Добавление ссылки на видео, если она не пустая
        if url_video:
            response += f"[Video]({url_video})\n"
        # Добавление ссылки на пост, если она не пустая
        if url_post:
            response += f"[Post]({url_post})\n"

        # Отправка ответа пользователю с использованием Markdown
        await message.reply(response, parse_mode=ParseMode.MARKDOWN)
    else:

        # Если записи не найдены, отправить соответствующее сообщение
        await message.reply("Видимо в базе данных еще нет ни одной статьи🤷️\n"
                            "Попробуйте немного подождать⏳\n"
                            "Примерно 20 секунд\n"
                            "Если же и это не помогло,\n"
                            "ты всегда можешь обратиться к человеку который написал это чудо😁")


async def send_latest_7_articles(message: types.Message):
    articles = await get_latest_7_articles()

    if articles:
        for article in articles:
            await asyncio.sleep(2)
            slug, title, subtitle, body, url_img, url_video, url_post, datetime = article
            response = f"*{title}*\n\n"
            if subtitle:
                response += f"{subtitle}\n\n"
            if body:
                response += f"{body}\n\n"
            if url_img:
                response += f"[Image]({url_img})\n"
            if url_video:
                response += f"[Video]({url_video})\n"
            if url_post:
                response += f"[Post]({url_post})\n"
            # Разбиваем сообщение на части, если оно слишком длинное
            while len(response) > 4096:
                split_index = response.rfind('\n', 0, 4096)
                if split_index == -1:
                    split_index = 4096
                part_to_send = response[:split_index]

                # Проверяем и корректируем Markdown-разметку
                if part_to_send.count('*') % 2 != 0:
                    part_to_send += '*'
                    response = response[split_index + 1:]
                else:
                    response = response[split_index:]

                await message.reply(part_to_send, parse_mode=ParseMode.MARKDOWN)

            # Отправляем оставшуюся часть сообщения
            if response:
                await message.reply(response, parse_mode=ParseMode.MARKDOWN)

    else:
        await message.reply("К сожалению, не удалось найти 7 последних статей.")


async def search_article(message: types.Message):
    # Получаем аргументы команды
    args = message.get_args()

    # Проверяем, есть ли аргументы после команды
    if not args.strip():
        # Если аргументы отсутствуют, отправляем сообщение пользователю
        await message.reply("Введите ключевое слово после /search")
        return

    # Выполняем поиск
    articles = await search_articles_by_keyword(args.strip())

    # Проверяем, есть ли результаты
    if articles:
        for article in articles:
            slug, title, subtitle, body, url_img, url_video, url_post, datetime = article
            response = f"*{title}*\n\n"
            if subtitle:
                response += f"{subtitle}\n\n"
            if body:
                response += f"{body}\n\n"
            if url_img:
                response += f"[Image]({url_img})\n"
            if url_video:
                response += f"[Video]({url_video})\n"
            if url_post:
                response += f"[Post]({url_post})\n"
            await message.reply(response, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply(f"По запросу '{args.strip()}' ничего не найдено.")


async def handle_unknown_message(message: types.Message):
    """
    Обработчик для всех остальных сообщений, которые не соответствуют командам.
    Args: message (types.Message): Объект сообщения.
    """
    await message.reply("Я не могу найти данную команду у себя в блокнотике, но ты можешь попробовать еще раз😉")
