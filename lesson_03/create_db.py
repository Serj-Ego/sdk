import sqlite3
from sqlite3 import Error


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
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255),
        subtitle VARCHAR(255),
        body TEXT,
        img_url TEXT,
        datetime DATETIME
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Таблица news успешно создана или уже существует.")
    except Error as e:
        print(f"Ошибка при создании таблицы: {e}")


def main():
    database = "news_database.db"

    # Создать соединение с базой данных
    conn = create_connection(database)

    # Создать таблицу news
    if conn is not None:
        create_table(conn)
    else:
        print("Ошибка! Невозможно создать соединение с базой данных.")

    # Закрыть соединение
    if conn:
        conn.close()


if __name__ == '__main__':
    main()
