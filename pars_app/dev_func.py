import os


def write_page_html(main_page: str, dir_name: str, file_name: str) -> None:
    """
    Записывает содержимое страницы новостей в файл, создавая необходимый каталог, если он отсутствует.

    :param main_page: Текстовое содержимое страницы новостей.
    :param dir_name: Имя каталога, в который будет сохранен файл.
    :param file_name: Имя файла, в который будет записано содержимое страницы.
    """

    # Создаем каталог, если он отсутствует
    os.makedirs(dir_name, exist_ok=True)

    # Записываем текст в файл
    with open(f"{dir_name}/{file_name}", "w", encoding="utf-8") as file:
        file.write(main_page)


def read_page_html(dir_name: str, file_name: str) -> str:
    """
    Читает содержимое HTML-файла из указанного каталога и возвращает его как строку.

    :param dir_name: Название каталога, где хранится файл.
    :param file_name: Название HTML-файла для чтения.
    :return: Содержимое файла в виде строки.
    """
    with open(f"{dir_name}/{file_name}", "r", encoding="utf-8") as file:
        page = file.read()
        # print(page)  # TODO: print
        return page
