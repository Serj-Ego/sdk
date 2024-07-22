import sqlite3
from sqlite3 import Error
import json


def create_connection(db_file):
    """Создает соединение с базой данных SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Соединение установлено с SQLite версией: {sqlite3.version}")
    except Error as e:
        print(f"Ошибка при подключении к SQLite: {e}")
    return conn


def create_table(conn):
    """Создает таблицу news, если она не существует."""
    try:
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) UNIQUE,
            subtitle VARCHAR(255),
            body TEXT,
            img_url TEXT,
            datetime TEXT
        )
        """
        cur = conn.cursor()
        cur.execute(sql_create_table)
        print("Таблица 'news' успешно создана или уже существует.")
    except Error as e:
        print(f"Ошибка при создании таблицы: {e}")


def insert_or_update_news(conn, title, subtitle, body, img_url, datetime_str):
    """Вставляет или обновляет запись в таблице news."""
    sql = """
    INSERT OR REPLACE INTO news (title, subtitle, body, img_url, datetime)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, (title, subtitle, body, img_url, datetime_str))
        conn.commit()
        print("Запись успешно вставлена или обновлена.")
    except Error as e:
        print(f"Ошибка при вставке или обновлении записи: {e}")


def main():
    # Путь к JSON-файлу
    json_file = 'news_data.json'

    # Загрузка данных из JSON-файла
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    title = data.get('title')
    subtitle = data.get('subtitle')
    body = data.get('body')
    img_url = data.get('img_url')
    datetime_str = data.get('time_meta')

    database = "news_database.db"

    # Создать соединение с базой данных
    conn = create_connection(database)

    if conn:
        # Создать таблицу, если не существует
        create_table(conn)

        # Вставить или обновить запись
        insert_or_update_news(conn, title, subtitle, body, img_url, datetime_str)

        # Закрыть соединение
        conn.close()
    else:
        print("Ошибка! Невозможно создать соединение с базой данных.")


if __name__ == '__main__':
    main()
