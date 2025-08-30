import psycopg2
from config import DB_NAME, DB_USER, DB_PORT, DB_HOST, DB_PASSWORD
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from src.api import get_vacancies, get_companies, get_companie_info



def create_database_if_not_exists() -> None:
    """
        Создание БД если не существует
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database="postgres", # Подключаемся к стандартной БД
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        with conn.cursor() as cur:
            cur.execute(f"select 1 from pg_database where datname={DB_NAME}")
            exists = cur.fetchone()

            if not exists:
                cur.execute(f"CREATE DATABASE {DB_NAME}")
                print(f"Создана база данных БД: {DB_NAME}")
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
    finally:
        if 'conn' in locals():
            conn.close()


def get_db_connection():
    create_database_if_not_exists()
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER,password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )



def insert_data(companie_ids):
    """
        Создаем таблицы employees и vacancies
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            for company_id in companie_ids:
                info = get_companie_info(company_id)
                print(f"Добавляем компанию: {info["name"]} {info["id"]} {info["alternate_url"]} {info["vacancies_url"]} {info["open_vacancies"]}"],

            cur.execute(
                """
                    INSERT INFO public.companies(id, name, alternate_url, vacancies_url, open_vacancies)
                    VALUES(?, ?, ?, ?, ?);
                """
            )