import psycopg2
from psycopg2 import Error


def create_connection(db_name, db_user, db_password, db_host, db_port):
    """Создает соединение с базой данных PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print(f"Соединение установлено с PostgreSQL версией: {conn.server_version}")
    except Error as e:
        print(f"Ошибка при подключении к PostgreSQL: {e}")
    return conn


def create_database(db_user, db_password, db_host, db_port, db_name):
    """Создает базу данных, если она не существует."""
    try:
        # Подключение к серверу PostgreSQL без указания базы данных
        conn = psycopg2.connect(
            dbname='postgres',
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE DATABASE {db_name}")
            print(f"База данных {db_name} успешно создана.")
        else:
            print(f"База данных {db_name} уже существует.")
        cur.close()
        conn.close()
    except Error as e:
        print(f"Ошибка при создании базы данных: {e}")


def create_table(conn):
    """Создает таблицу news_articles с указанными полями и составным первичным ключом."""
    try:
        create_db = """
        CREATE TABLE IF NOT EXISTS news_articles (
            slug VARCHAR(255),
            title VARCHAR(255),
            subtitle VARCHAR(255),
            body TEXT,
            url_img TEXT,
            url_video TEXT,
            url_post TEXT,
            datetime TIMESTAMP,
            PRIMARY KEY (slug, datetime)
        );
        """
        cur = conn.cursor()
        cur.execute(create_db)
        conn.commit()
        print("Таблица news_articles успешно создана.")
    except Error as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        cur.close()


def main():
    database = {
        'db_name': 'pars_db',
        'db_user': 'postgres',
        'db_password': '123',
        'db_host': 'localhost',
        'db_port': '5432'
    }

    # Создать базу данных, если она не существует
    create_database(database['db_user'], database['db_password'], database['db_host'], database['db_port'], database['db_name'])

    # Создать соединение с базой данных
    conn = create_connection(database['db_name'], database['db_user'], database['db_password'], database['db_host'], database['db_port'])

    # Создать таблицу, если соединение успешно установлено
    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        print("Ошибка! Невозможно создать соединение с базой данных.")


if __name__ == '__main__':
    main()
