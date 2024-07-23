import psycopg2
from psycopg2 import Error


def add_or_update_article(slug, title, subtitle, body, url_img, url_video, url_post, datetime_str):
    """
    Добавляет или обновляет запись в таблице 'news_articles' базы данных PostgreSQL.

    :param slug: Уникальный идентификатор статьи.
    :param title: Заголовок статьи.
    :param subtitle: Подзаголовок статьи.
    :param body: Тело статьи.
    :param url_img: URL изображения статьи.
    :param url_video: URL видео статьи.
    :param url_post: URL поста статьи.
    :param datetime_str: Дата и время статьи в формате строки.
    """

    # Параметры подключения к базе данных
    database = {
        'dbname': 'pars_db',
        'user': 'postgres',
        'password': '123',
        # 'host': 'localhost',
        'host': 'db',
        'port': '5432'
    }

    try:
        # Установить соединение с базой данных
        conn = psycopg2.connect(**database)
        cursor = conn.cursor()

        # SQL-запрос для вставки или обновления записи
        sql_insert_or_update = """
        INSERT INTO news_articles (slug, title, subtitle, body, url_img, url_video, url_post, datetime)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT(slug, datetime) DO UPDATE SET
            title = EXCLUDED.title,
            subtitle = EXCLUDED.subtitle,
            body = EXCLUDED.body,
            url_img = EXCLUDED.url_img,
            url_video = EXCLUDED.url_video,
            url_post = EXCLUDED.url_post;
        """

        # Выполнить SQL-запрос с передачей значений
        cursor.execute(sql_insert_or_update, (slug, title, subtitle, body, url_img, url_video, url_post, datetime_str))

        # Зафиксировать изменения
        conn.commit()

        print("Запись успешно добавлена или обновлена.")

    except Error as e:
        print(f"Ошибка при работе с PostgreSQL: {e}")
    finally:
        if conn:
            # Закрыть соединение с базой данных
            cursor.close()
            conn.close()

# # Пример вызова функции
# add_or_update_article('example_slug', 'Example Title', 'Example Subtitle', 'Example Body',
#                       'http://example.com/image.jpg', 'http://example.com/video.mp4', 'http://example.com/post',
#                       '2023-07-24 10:00:00')
