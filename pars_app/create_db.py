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
    """Создает таблицу news_articles с указанными полями и составным первичным ключом."""
    try:
        create_db = """
        CREATE TABLE IF NOT EXISTS news_articles (
            slug VARCHAR(255),
            title VARCHAR(255),
            subtitle VARCHAR(255),
            body TEXT,
            url_img URL,
            url_video URL,
            datetime DATETIME,
            PRIMARY KEY (slug, datetime)
        );
        """
        cur = conn.cursor()
        cur.execute(create_db)
        print("Таблица news_articles успешно создана.")
    except Error as e:
        print(f"Ошибка при создании таблицы: {e}")


def main():
    database = "test_db.sqlite"

    # Создать соединение с базой данных
    conn = create_connection(database)

    # Создать таблицу, если соединение успешно установлено
    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        print("Ошибка! Невозможно создать соединение с базой данных.")


if __name__ == '__main__':
    main()
