import os
import json

import requests
from bs4 import BeautifulSoup

URL = "https://www.mk.ru/news/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/126.0.0.0 Safari/537.36"
}
FILE_PATH_MAIN_NEWS_PAGE = "pars_html/main_news_page.html"

FILES_PATH_SINGLE_NEWS_PAGE = "pars_html/single_pages"


def get_page(url: str, http_headers: dict) -> str:
    response = requests.get(url, headers=http_headers)
    return response.text


def write_main_page_html(main_page: str) -> None:
    # Создаем каталог, если он отсутствует
    os.makedirs("pars_html", exist_ok=True)

    # Записываем текст в файл
    with open("pars_html/main_news_page.html", "w") as file:
        file.write(main_page)


def parse_main_page(file_path: str) -> list:  # TODO: Заменить название аргумента 'file_path'
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            src = file.read()
            # print('with')  # TODO: print

        news_urls_list = []

        # Принимает страницу html и парсер
        soup = BeautifulSoup(src, 'lxml')

        # Находит первый тег <ul> с классом 'news-listing__day-list' в котором содержится список постов
        list_items = soup.find('ul', class_='news-listing__day-list')
        # print(list_items)  # TODO: print

        # Находит все теги <li> с классом 'news-listing__item' внутри тега <ul>
        # В каждом теге <li> содержится информация об одном посте
        # print('list_items.find_all')  # TODO: print
        news_items = list_items.find_all('li', class_='news-listing__item')
        # print('before list_items.find_all')  # TODO: print

        cnt = 0  # Тестовая переменная TODO: Удалить переменную

        # Проходит по каждому элементу <li> в списке 'news_items' и достает ссылку
        for news in news_items:
            # region Description
            #   TODO: Изменить или удалить описание
            """
            news содержит:
                <a class="news-listing__item-link"> - ссылка на пост
                    в котором:
                    <span class="news-listing__item-time"> - ВРЕМЯ ПОСТА
                    <h3 class="news-listing__item-title "> - Заголовок поста
            """
            #   TODO: Горячие новости
            # cls_lst = news.get('class')  # Если содержится класс 'news-listing__item_hot' то новость 'горячая'

            #   TODO: Принт каждой новости
            # print(news.find('a', class_='news-listing__item-link')['href'])
            # endregion

            #   Создает список ссылок на посты
            news_urls_list.append(news.find('a', class_='news-listing__item-link')['href'])

            cnt += 1  # Тестовая переменная TODO: Удалить переменную

        # print(cnt)  # Тестовая переменная TODO: Удалить переменную

        return news_urls_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return []  # Возвращает пустой список в случае ошибки


def get_single_page(news_urls_list: list, http_headers: dict) -> str:
    single_page_dict = {}
    for news_url in news_urls_list[0:1]:  # TODO Срез на списке (для тестирования)
        # slug_title = str(news_url).split('/')[-1].split('.')[-2]

        # url_path_segments = news_url.split('/')
        # last_index_after_slash = url_path_segments[-1]
        # last_index_segments = last_index_after_slash.split('.')
        # title_slug = last_index_segments[-2]
        #
        # single_page_dict[title_slug] = requests.get(news_url, headers=http_headers)
        # print(single_page_dict)

        # print(title_slug)
        # print(slug_title)
        response = requests.get(news_url, headers=http_headers)

        # print(response.text)

        yield response.text

        # yield single_page_dict


def write_single_page_html(single_page: dict) -> None:  # TODO: Не используется
    # Создаем каталог, если он отсутствует
    os.makedirs("pars_html", exist_ok=True)
    os.makedirs("pars_html/single_pages", exist_ok=True)

    title_slug = list(single_page.keys())[0]
    print(title_slug)
    text_post = single_page[title_slug]
    print(text_post.text)

    with open(f"pars_html/single_pages/{title_slug}.html", "w") as file:
        file.write(text_post.text)


def read_single_page_html(path: str) -> object:  # TODO: Не используется
    files = os.listdir(path)
    for file in files:
        # print(file)
        with open(f'pars_html/single_pages/{file}', 'r') as fl:
            single_page_html = fl.read()

            # soup = BeautifulSoup(single_page_html, 'lxml')

        # yield soup

        # yield single_page_html


def parse_single_page(url: str, http_headers: dict):  # TODO: Разработка

    news_dict = {}

    # class Post:  # TODO: Не используемый объект
    #     def __init__(self, title, subtitle, body, url_img, time_meta):
    #         self.title = title
    #         self.subtitle = subtitle
    #         self.body = body
    #         self.url_img = url_img
    #         self.time_meta = time_meta

    # print(single_page_html.text)

    # print(get_page(url, http_headers))

    soup = BeautifulSoup(get_page(url, http_headers), 'lxml')

    # content
    article_grid_content = soup.find('div', class_='article-grid__content')
    main_article = article_grid_content.find('main', class_='article')

    # header
    article_header = main_article.find('header', class_='article__header')
    title = article_header.find('h1', class_='article__title').text
    print(title)  # TODO: print
    news_dict['title'] = title
    subtitle = article_header.find('p', class_='article__subtitle').text
    print(subtitle)  # TODO: print
    news_dict['subtitle'] = subtitle

    # body
    paragraph = []
    article_body = main_article.find('div', class_='article__body')
    paragraph_list = article_body.find_all('p')
    for p in paragraph_list:
        paragraph.append(p.text)

    body = '\n\n'.join(paragraph)
    print(body)  # TODO: print
    news_dict['body'] = body

    # img
    url_img = main_article.find('img', class_='article__picture-image').get('src')
    print(url_img)  # TODO: print
    news_dict['url_img'] = url_img

    # datetime
    article__meta = main_article.find('div', class_='article__meta').find('p', class_='meta meta_article')
    time_meta = article__meta.find('time', class_='meta__text').get('datetime')
    print(time_meta)  # TODO: print
    news_dict['time_meta'] = time_meta

    print(news_dict)

    # Путь к JSON-файлу
    json_file_path = 'news_data.json'

    # Запись словаря в JSON-файл
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(news_dict, json_file, ensure_ascii=False, indent=4)





    # print(soup.find('header', class_='article__header').find('h1', class_='article__title').text)

    # try:
    #     soup = BeautifulSoup('', 'lxml')
    #     print(soup)

        # soup = BeautifulSoup(src, "lxml")
        # print(soup)
        # print(soup.find('header', class_='article__header').find('h1', class_='article__title').text)

    # except Exception as e:
    #     print(f"An error occurred: {e}")
    # pass


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/126.0.0.0 Safari/537.36"
    }

    # region request
    # req = requests.get(url, headers)
    # print(req.text)

    # with open("lesson_03.html", "w") as file:
    #     file.write(req.text)
    # endregion

    with open("lesson_03.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    lis = soup.find_all("li", class_="news-listing__item")
    # print(lis)

    posts_urls = []
    # Получение тега "li"[пункт] из тега "ul"[лист] и сохранение ссылки в список
    for li in lis:
        post_url = li.find("a", class_="news-listing__item-link").get("href")
        # print(post_url)
        posts_urls.append(post_url)

    for url_one in posts_urls[0:1]:
        req = requests.get(url_one, headers=headers)
        post_name = url_one.split('/')[-1].split('.')[-2]

        # Запись новостной html страницы в каталог "data" и присвоение имени "post_name"
        with open(f"data/{post_name}.html", "w") as file:
            file.write(req.text)

        # Чтение записанной новостной html страницы с названием "post_name" из каталога "data"
        with open(f"data/{post_name}.html") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        article__title = soup.find('h1', class_='article__title')
        article__body = soup.find_all('div', class_='article__body')

        print(article__title)
        print(article__body)


if __name__ == "__main__":
    # get_html(URL)

    # get_main_page(URL, HEADERS)
    # write_main_page_html(get_main_page(URL, HEADERS))
    # parse_main_page(FILE_PATH_MAIN_NEWS_PAGE)

    # get_single_page(parse_main_page(FILE_PATH_MAIN_NEWS_PAGE), HEADERS)

    # for i in get_single_page(parse_main_page(FILE_PATH_MAIN_NEWS_PAGE), HEADERS):
    #     write_single_page_html(i)

    # single_pages = read_single_page_html(FILES_PATH_SINGLE_NEWS_PAGE)
    # for single_page in single_pages:
    #     parse_single_page(single_page)
        # print(single_page)
    # print(read_single_page_html(FILES_PATH_SINGLE_NEWS_PAGE))

    url_lst = parse_main_page(FILE_PATH_MAIN_NEWS_PAGE)
    for url in url_lst[0:1]:
        parse_single_page(url, HEADERS)

    # write_single_page_html()
    # pass
