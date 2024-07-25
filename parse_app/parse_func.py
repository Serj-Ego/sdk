import aiohttp
from bs4 import BeautifulSoup
from slugify import slugify
import asyncio
import random


async def get_page(url: str, http_headers: dict) -> dict:
    """
    Выполняет асинхронный HTTP GET запрос по указанному URL с заданными заголовками
    и возвращает содержимое ответа в виде текста.

    :param url: URL веб-страницы, которую нужно получить.
    :param http_headers: Словарь HTTP заголовков для запроса.
    :return: Содержимое ответа в виде текста.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=http_headers) as response:
            text = await response.text()
            return {'response': text, 'url': url}


async def parse_main_page(page_text: str) -> list:
    """
    Парсит HTML-содержимое основной страницы новостей и извлекает ссылки на отдельные новости.

    :param page_text: HTML-содержимое страницы в виде строки.
    :return: Список ссылок на новости. Возвращает пустой список в случае ошибки.
    """
    try:

        news_urls_list = []

        soup = BeautifulSoup(page_text, 'lxml')

        # Получение списка статей за день
        news_day_list = soup.find('ul', class_='news-listing__day-list')

        # Получение всех статей из списка "news_day_list"
        news_items = news_day_list.find_all('li', class_='news-listing__item')

        # Создание списка url адресов статей
        for news in news_items:
            news_urls_list.append(news.find('a', class_='news-listing__item-link')['href'])

        return news_urls_list

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


async def get_single_page(news_urls_list: list, http_headers: dict) -> list:
    """
    Генерирует содержимое страниц новостей по заданным URL.

    :param news_urls_list: Список URL-адресов новостей.
    :param http_headers: Заголовки HTTP-запросов.
    :return: Список HTML-кодов страниц новостей.
    """
    tasks = []
    async with aiohttp.ClientSession() as session:
        for news_url in news_urls_list:
            tasks.append(fetch_page(session, news_url, http_headers))
        return await asyncio.gather(*tasks)


async def fetch_page(session, url, headers):
    """
    Асинхронно получает HTML-код страницы новости.

    :param session: Асинхронная сессия aiohttp.
    :param url: URL страницы.
    :param headers: HTTP-заголовки.
    :return: Словарь с URL и содержимым страницы.
    """
    # Задержка на случайное время (сайты не любят когда их парсят)
    await asyncio.sleep(random.uniform(4, 8))  # Задержка на случайное время
    async with session.get(url, headers=headers) as response:
        text = await response.text()
        return {'response': text, 'url': url}


def parse_single_page(page_dict: dict) -> dict:
    """
    Парсит страницу новости и извлекает заголовок, подзаголовок, тело, изображение, видео и дату публикации.

    :param page_dict: Словарь с HTML-кодом страницы и URL.
    :return: Словарь с данными новости.
    """
    # Получение контента страницы
    page = page_dict['response']

    news_dict = {}

    # Создание объекта BeautifulSoup с передачей аргументов (страница и модель парсера)
    soup = BeautifulSoup(page, 'lxml')

    # Извлечение основного тега статьи
    main_article = soup.find('main', class_='article')

    # Извлечение всех заголовков статьи
    article_header = main_article.find('header', class_='article__header')

    # Извлечение основного заголовка статьи
    title = article_header.find('h1', class_='article__title')
    news_dict['title'] = title.text if title else None

    # Извлечение подзаголовка статьи
    subtitle = article_header.find('p', class_='article__subtitle')
    news_dict['subtitle'] = subtitle.text if subtitle else None

    # Преобразования заголовка в slug
    news_dict['slug'] = slugify(title.text) if title else None

    # Извлечение тела статьи
    paragraph_list = []
    article_body = main_article.find('div', class_='article__body')

    # Получение всех параграфов статьи
    paragraph_list_row = article_body.find_all('p')

    # Извлечение текста из параграфов
    for p in paragraph_list_row:
        paragraph_list.append(p.text)

    # Проверка количества элементов (параграфов) в списке
    news_dict['body'] = '\n\n'.join(paragraph_list) if len(paragraph_list) > 1 else paragraph_list[0]

    # Извлечение ссылки на изображение (None если тег отсутствует)
    url_img = main_article.find('img', class_='article__picture-image')
    news_dict['url_img'] = url_img.get('src') if url_img else None

    # Извлечение ссылки на видео (None если тег отсутствует)
    article_video = article_body.find('div', class_='article-incut__video-content-place')
    news_dict['url_video'] = article_video.find('link', itemprop='contentUrl').get('href') if article_video else None

    # Извлечение даты публикации (None если тег отсутствует)
    article_meta = main_article.find('div', class_='article__meta')
    news_dict['datetime'] = article_meta.find('meta', itemprop='datePublished').get('content') if article_meta else None

    # Извлечение ссылки на пост из аргумента функции
    news_dict['url_post'] = page_dict['url']
    return news_dict

