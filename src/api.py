from typing import List, Dict
import requests

HH_API_URL = "https://api.hh.ru"


def get_companies() -> List[Dict]:
    """
        Получение списка всех компаний
    """
    url = f"{HH_API_URL}/employers"
    response = requests.get(url)

    if response.status_code != 200:
        print("Не удалось получить данные о компании")
        return []

    companies = response.json().get("items", [])

    if not companies:
        print("Список компаний пуст")

    return companies


def get_companie_info(company_id: str) -> Dict:
    """
        Получение информации о компании
    """
    url = f"{HH_API_URL}/employers/{company_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Не удалось получить данные о компании с id {company_id}")
        return {}

    return response.json()


def get_vacancies(company_id: str) -> List[Dict]:
    """
        Получение вакансий по id компании
    """
    url = f"{HH_API_URL}/vacancies"
    params = {
        "employer_id": company_id,
        "per_page": 100
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Не удалось получить вакансии для компании с id {company_id}")
        return []

    vacancies = response.json().get("items", [])
    print(f"Полученные вакансии: {vacancies}")

    if not vacancies:
        print(f"Список вакансий для компании с id {company_id} пуст.")

    return vacancies