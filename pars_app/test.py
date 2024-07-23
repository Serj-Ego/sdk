import settings, dev_settings
from parse_func import get_page, parse_main_page, get_single_page, parse_single_page
from dev_func import write_page_html, read_page_html


# Получение основной страницы
# main_page = get_page(settings.URL, settings.HEADERS)

# Запись основной страницы в файл  # TODO: dev function
# write_page_html(page, dev_settings.DIR_NAME, dev_settings.FILE_NAME)

# Чтение основной страницы  # TODO: dev function
main_page = read_page_html(dev_settings.DIR_NAME, dev_settings.FILE_NAME)

# Парсинг основной страницы и получение списка url каждой новости
url_list_single_pages = parse_main_page(main_page)

# Получение подробных страниц новостей
for single_page in get_single_page(url_list_single_pages, settings.HEADERS):
    for key, value in parse_single_page(single_page).items():
        print(f"{key}: {value}")
    print('============================')
    # print(parse_single_page(single_page))
