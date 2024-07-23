import requests
from bs4 import BeautifulSoup
from slugify import slugify
# from datetime import datetime

# from settings import URL, HEADERS


def get_page(url: str, http_headers: dict) -> str:
    """
    Выполняет HTTP GET запрос по указанному URL с заданными заголовками и возвращает содержимое ответа в виде текста.

    :param url: URL веб-страницы, которую нужно получить.
    :param http_headers: Словарь HTTP заголовков для запроса.
    :return: Содержимое ответа в виде текста.
    """
    response = requests.get(url, headers=http_headers)
    return response.text


def parse_main_page(page: str) -> list:
    """
    Парсит HTML-содержимое основной страницы новостей и извлекает ссылки на отдельные новости.

    :param page: HTML-содержимое страницы в виде строки.
    :return: Список ссылок на новости. Возвращает пустой список в случае ошибки.
    """
    try:
        news_urls_list = []

        # Создание объекта BeautifulSoup с передачей аргументов (страница и модель парсера)
        soup = BeautifulSoup(page, 'lxml')

        # Находит первый тег <ul> с классом 'news-listing__day-list' в котором содержится список постов
        list_items = soup.find('ul', class_='news-listing__day-list')

        # Находит все теги <li> с классом 'news-listing__item' внутри тега <ul>
        # В каждом теге <li> содержится информация об одном посте
        news_items = list_items.find_all('li', class_='news-listing__item')

        # Проходит по каждому элементу <li> в списке 'news_items' и достает ссылку
        for news in news_items:
            #   Создает список ссылок на посты
            news_urls_list.append(news.find('a', class_='news-listing__item-link')['href'])

        return news_urls_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return []  # Возвращает пустой список в случае ошибки


def get_single_page(news_urls_list: list, http_headers: dict) -> str:
    """
    Генерирует содержимое страниц новостей по заданным URL.

    :param news_urls_list: Список URL-адресов новостей.
    :param http_headers: Заголовки HTTP-запросов.
    :yield: HTML-код страницы новости.
    """
    for news_url in news_urls_list[0:3]:  # TODO Срез на списке (для тестирования)
        yield get_page(news_url, http_headers)


def parse_single_page(page: str):  # TODO: Разработка
    """
    Парсит страницу новости и извлекает заголовок, подзаголовок, тело, изображение, видео и дату публикации.

    :param page: Строка, содержащая HTML-код страницы новости.
    :return: Словарь с данными новости, включая заголовок, подзаголовок, тело, изображение, видео и дату публикации.
    """
    news_dict = {}

    # TODO: ⇓ Тестовый регион кода
    # region get test page
    # u = 'https://www.mk.ru/politics/2024/07/23/general-raskryl-chto-proizoshlo-s-vsu-pod-kharkovom.html'
    # test_post = get_page(u, HEADERS)
    # soup = BeautifulSoup(test_post, 'lxml')
    # endregion

    soup = BeautifulSoup(page, 'lxml')  # TODO: prod экземпляр

    # Извлечение основного тега статьи
    main_article = soup.find('main', class_='article')

    # Извлечение заголовкОВ статьи
    article_header = main_article.find('header', class_='article__header')

    # Извлечение заголовкА статьи
    title = article_header.find('h1', class_='article__title')
    news_dict['title'] = title.text if title else None

    # Извлечение подзаголовка статьи
    subtitle = article_header.find('p', class_='article__subtitle')
    news_dict['subtitle'] = subtitle.text if subtitle else None

    # Преобразования заголовка в slug # TODO: slug dev
    news_dict['slug'] = slugify(title.text) if title else None

    # Извлечение тела статьи
    paragraph_list = []
    article_body = main_article.find('div', class_='article__body')  # Тег содержащий тело статьи

    # Получение всех параграфов статьи
    paragraph_list_row = article_body.find_all('p')

    # Извлечение текста из параграфов
    for p in paragraph_list_row:
        paragraph_list.append(p.text)

    # Проверка количества элементов (параграфов) в списке
    if len(paragraph_list) > 1:
        body = '\n\n'.join(paragraph_list)
        # print(body)  # TODO: Print
        news_dict['body'] = body
    else:
        news_dict['body'] = paragraph_list[0]

    # Извлечение изображения
    url_img = main_article.find('img', class_='article__picture-image')
    news_dict['url_img'] = url_img.get('src') if url_img else None

    # Извлечение видео
    # Тег содержащий информацию по видео контенту
    article_incut_video = article_body.find('div', class_='article-incut__video-content-place')
    if article_incut_video:  # Проверка наличия тега 'article-incut__video-content-place'
        # Тег содержащий ссылку на виде
        video_link = article_incut_video.find('link', itemprop='contentUrl')
        # Получение ссылка на видео
        news_dict['url_video'] = video_link.get('href')
    else:
        news_dict['url_video'] = None

    # Извлечение даты публикации
    article_meta = main_article.find('div', class_='article__meta')  # Тег метаданных
    if article_meta:
        article_time_str = article_meta.find('meta', itemprop='datePublished').get('content')
        news_dict['datetime'] = article_time_str
    else:
        news_dict['datetime'] = None

    return news_dict
