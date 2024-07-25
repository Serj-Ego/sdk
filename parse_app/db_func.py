import aiosqlite
import sqlite3
from settings import DATABASE
from slugify import slugify


async def add_or_update_article(slug, title, subtitle, body, url_img, url_video, url_post, datetime_str):
    """
    Добавляет или обновляет запись в таблице 'news_articles' базы данных SQLite.

    :param slug: Уникальный идентификатор статьи.
    :param title: Заголовок статьи.
    :param subtitle: Подзаголовок статьи.
    :param body: Тело статьи.
    :param url_img: URL изображения статьи.
    :param url_video: URL видео статьи.
    :param datetime_str: Дата и время статьи в формате строки.
    """
    try:
        async with aiosqlite.connect(DATABASE) as db:
            async with db.cursor() as cursor:
                sql_insert_or_update = """
                INSERT INTO news_articles (slug, title, subtitle, body, url_img, url_video, url_post, datetime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(slug, datetime) DO UPDATE SET
                    title=excluded.title,
                    subtitle=excluded.subtitle,
                    body=excluded.body,
                    url_img=excluded.url_img,
                    url_video=excluded.url_video,
                    url_post=excluded.url_post;
                """
                await cursor.execute(sql_insert_or_update,
                                     (slug, title, subtitle, body, url_img, url_video, url_post, datetime_str))
                await db.commit()
                print("Запись успешно добавлена или обновлена.")
    except Exception as e:
        print(f"Ошибка при работе с SQLite: {e}")


def get_latest_article():
    """
    Получает последнюю статью из базы данных по дате и времени.
    Returns: tuple: Кортеж с данными статьи или None, если статьи не найдены.
    """
    try:
        # Подключение к базе данных
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Выполнение SQL-запроса для получения последней записи по дате и времени
        cursor.execute("""
            SELECT slug, title, subtitle, body, url_img, url_video, url_post, datetime 
            FROM news_articles 
            ORDER BY datetime DESC 
            LIMIT 1
        """)
        # Извлечение одной записи из результата запроса
        article = cursor.fetchone()

        # Закрытие соединения с базой данных
        conn.close()

        return article

    except sqlite3.Error as e:
        # Обработка ошибок работы с базой данных
        print(f"Ошибка БД: {e}")
        return None

    except Exception as e:
        # Обработка других ошибок
        print(f"Ошибка: {e}")
        return None


async def get_latest_7_articles() -> list:
    try:
        async with aiosqlite.connect(DATABASE) as db:
            async with db.cursor() as cursor:
                await cursor.execute("""
                    SELECT slug, title, subtitle, body, url_img, url_video, url_post, datetime 
                    FROM news_articles 
                    ORDER BY datetime DESC 
                    LIMIT 7
                """)
                articles = await cursor.fetchall()
                return articles
    except Exception as e:
        print(f"Ошибка при работе с SQLite: {e}")
        lst = []
        return lst


async def search_articles_by_keyword(keyword: str):
    """
        Функция поиска статей по ключевому слову в заголовке.

        Эта асинхронная функция подключается к базе данных SQLite, выполняет запрос для поиска статей,
        заголовок которых содержит указанное ключевое слово, и возвращает найденные статьи.

        Аргументы: keyword (str): Ключевое слово для поиска в заголовках статей.

        Возвращает: list: Список найденных статей,
        где каждая статья представлена в виде кортежа значений
        (slug, title, subtitle, body, url_img, url_video, url_post, datetime).

        Обработка исключений:
        В случае ошибки при работе с базой данных функция выведет сообщение об ошибке и вернет пустой список.

        Примечание:
        Для поиска используется функция slugify,
        которая преобразует ключевое слово в URL-дружественный формат перед выполнением запроса.
        """
    # Функция поиска статей по ключевому слову в заголовке
    try:
        async with aiosqlite.connect(DATABASE) as db:
            async with db.cursor() as cursor:
                sql_search = """
                SELECT slug, title, subtitle, body, url_img, url_video, url_post, datetime
                FROM news_articles
                WHERE LOWER(slug) LIKE LOWER(?)
                """
                await cursor.execute(sql_search, (f'%{slugify(keyword).lower()}%',))
                articles = await cursor.fetchall()
                print(articles)
                return articles
    except Exception as e:
        print(f"Ошибка при работе с SQLite: {e}")
        return []
