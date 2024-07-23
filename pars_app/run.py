import schedule
import settings, dev_settings
from parse_func import get_page, parse_main_page, get_single_page, parse_single_page
# from dev_func import write_page_html, read_page_html  # TODO: dev function
from add_or_update_db import add_or_update_article


def get_articles():
    # Получение основной страницы
    main_page = get_page(settings.URL, settings.HEADERS)

    # Запись основной страницы в файл  # TODO: dev function
    # write_page_html(main_page, dev_settings.DIR_NAME, dev_settings.FILE_NAME)

    # Чтение основной страницы  # TODO: dev function
    # main_page = read_page_html(dev_settings.DIR_NAME, dev_settings.FILE_NAME)

    # Парсинг основной страницы и получение списка url каждой новости
    url_list_single_pages = parse_main_page(main_page)

    # Определение переменной с генератором (html страницы каждой новости)
    single_pages = get_single_page(url_list_single_pages, settings.HEADERS)

    for single_page in single_pages:
        article_dict = parse_single_page(single_page)
        add_or_update_article(
            db_file=dev_settings.DB_DIR,
            slug=article_dict['slug'],
            title=article_dict['title'],
            subtitle=article_dict['subtitle'],
            body=article_dict['body'],
            url_img=article_dict['url_img'],
            url_video=article_dict['url_video'],
            url_post=article_dict['url_post'],
            datetime_str=article_dict['datetime']
        )


def main():
    schedule.every(40).seconds.do(get_articles)
    # schedule.every(5).minutes.do(get_articles)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
