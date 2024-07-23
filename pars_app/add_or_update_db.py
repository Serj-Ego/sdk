import sqlite3
from sqlite3 import Error


def add_or_update_article(db_file, slug, title, subtitle, body, url_img, url_video, datetime_str):
    """
    Добавляет или обновляет запись в таблице 'news_articles' базы данных SQLite.

    :param db_file: Путь к файлу базы данных SQLite.
    :param slug: Уникальный идентификатор статьи.
    :param title: Заголовок статьи.
    :param subtitle: Подзаголовок статьи.
    :param body: Тело статьи.
    :param url_img: URL изображения статьи.
    :param url_video: URL видео статьи.
    :param datetime_str: Дата и время статьи в формате строки. # TODO: Дата и время статьи в формате строки
    """

    try:
        # Установить соединение с базой данных
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # SQL-запрос для вставки или обновления записи
        sql_insert_or_update = """
        INSERT INTO news_articles (slug, title, subtitle, body, url_img, url_video, datetime)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(slug, datetime) DO UPDATE SET
            title=excluded.title,
            subtitle=excluded.subtitle,
            body=excluded.body,
            url_img=excluded.url_img,
            url_video=excluded.url_video;
        """

        # Выполнить SQL-запрос с передачей значений
        cursor.execute(sql_insert_or_update, (slug, title, subtitle, body, url_img, url_video, datetime_str))

        # Зафиксировать изменения
        conn.commit()

        print("Запись успешно добавлена или обновлена.")  # TODO: Print

    except Error as e:
        print(f"Ошибка при работе с SQLite: {e}")
    finally:
        if conn:
            # Закрыть соединение с базой данных
            conn.close()
