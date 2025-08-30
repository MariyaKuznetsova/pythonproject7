import psycopg2
from config import DB_NAME, DB_USER, DB_PORT, DB_HOST, DB_PASSWORD
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from src.api import get_vacancies, get_companies, get_companie_info
from pprint import pprint
#from src.db_manager import
#from src.database import


if __name__ == "__main__":
    while True:
        print(
            """
            Меню действий
    1. Список компаний и вакансий
    2. Список всех вакансий
    3. Средняя зарплата
    4. Вакансия с зарплатой выше средней
    5. Поиск по ключевому слову
    6. Выход
            """
        )

        value = input('> ').strip()

        if value == '1':
            companies = db_manager.get_companies_and_vacancies_count()
            for company, industry, count in companies:
                points = '...' if len(industry) >= 40 else ''
                print(f'{company}: {count} вакансий\n{industry}{points}\n')

        elif value == '2':
            vacancies = db_manager.get_all_vacancies()
            for company, title, salary_from, salary_to, currency, url in vacancies:
                salary = ''
                if salary_from or salary_to:
                    salary = f'Зарплата {salary_from or '-'} - {salary_to or '-'} {currency}'
                print(f'{company} | {title} | {salary} | {url}')

        elif value == '3':
            vacancies = db_manager.get_avg_salary()
            print(f'Средняя зарплата: {.2}')

        elif value == '4':
            vacancies = db_manager.get_vacancies_with_higher_salary()
            for company, title, salary_from, salary_to, currency, url in vacancies:
                salary = f'Зарплата: {salary_from} - {salary_to} {currency}'
                print(f'{company} | {title} | {salary} | {url}')

        elif value == '5':
            keyword = input('Введите ключевое слово: ').strip()
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for company, title, salary_from, salary_to, currency, url in vacancies:
                salary = ''
                if salary_from or salary_to:
                    salary = f'Зарплата {salary_from or '-'} - {salary_to or '-'} {currency}'
                print(f'{company} | {title} | {salary} | {url}')

        elif value == '0':
            break
        else:
            print('Неверный ввод. Попробуйте снова.')






