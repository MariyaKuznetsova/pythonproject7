import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER, DB_NAME
from src.api import get_companie_info, get_vacancies
from src.database import create_database, insert_data, save_employer_to_db, save_vacancies_to_db
from src.db_manager import DBManager

def main() -> None:
    """Собираем данные о работодателях и вакансиях с hh.ru в базу данных"""
    # Подключение к БД
    db_params = {
        'host': DB_HOST,
        'database': 'postgres',
        'user': DB_USER,
        'password': DB_PASSWORD
    }
    db_name = DB_NAME

    # Создание БД
    create_database(db_params, db_name)
    db_params['database'] = db_name

    # Подключение к БД и создание таблиц
    conn = psycopg2.connect(**db_params)
    insert_data(conn)

    employer_id = ["1740", "1455", "4233", "1057", "1140", "3529", "2180", "125493", "15478", "64174"]

    for employer in employer_id:
        companies = get_companie_info(employer)
        if companies:
            save_employer_to_db(conn, companies)
            vacancies = get_vacancies(employer)
            save_vacancies_to_db(conn, vacancies, employer)
    conn.close()

def user_interaction() -> None:
    db_params = {
        "host": DB_HOST,
        "database": "postgres",
        "user": DB_USER,
        "password": DB_PASSWORD,
    }
    db_manager = DBManager(db_params)

    while True:
        print(
            """
            Выберите действие:
    1. Список компаний и вакансий
    2. Список всех вакансий
    3. Средняя зарплата
    4. Вакансия с зарплатой выше средней
    5. Поиск по ключевому слову
    6. Выход
            """
        )

        value = input("> ").strip()

        if value == "1":
            companies = db_manager.get_companies_and_vacancies_count()
            for company, industry, count in companies:
                points = "..." if len(industry) >= 40 else ""
                print(f"{company}: {count} вакансий\n{industry}{points}\n")

        elif value == "2":
            vacancies = db_manager.get_all_vacancies()
            for company, title, salary_from, salary_to, currency, url in vacancies:
                salary = ""
                if salary_from or salary_to:
                    salary = f"Зарплата {salary_from or '-'} - {salary_to or '-'} {currency}"
                print(f"{company} | {title} | {salary} | {url}")

        elif value == "3":
            vacancies = db_manager.get_avg_salary()
            vacancies_int = int(vacancies)
            print(f"Средняя зарплата: {vacancies_int}")

        elif value == "4":
            vacancies = db_manager.get_vacancies_with_higher_salary()
            for company, title, salary_from, salary_to, currency, url in vacancies:
                salary = f"Зарплата: {salary_from} - {salary_to} {currency}"
                print(f"{company} | {title} | {salary} | {url}")

        elif value == "5":
            keyword = input("Введите ключевое слово: ").strip()
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for company, title, salary_from, salary_to, currency, url in vacancies:
                salary = ""
                if salary_from or salary_to:
                    salary = f"Зарплата {salary_from or '-'} - {salary_to or '-'} {currency}"
                print(f"{company} | {title} | {salary} | {url}")

        elif value == "6":
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
    user_interaction()
