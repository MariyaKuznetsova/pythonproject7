from typing import Dict, List

import requests

HH_API_URL = "https://api.hh.ru"


def get_companies() -> List[Dict]:
    """
    Получение списка всех компаний
    """
    url = f"{HH_API_URL}/employers"
    response = requests.get(url)

    if response.status_code != 200:

        return []

    companies = response.json().get("items", [])



    return companies


def get_companie_info(company_id: str) -> Dict:
    """
    Получение информации о компании
    """
    url = f"{HH_API_URL}/employers/{company_id}"
    response = requests.get(url)

    if response.status_code != 200:

        return {}

    return response.json()


def get_vacancies(company_id: str) -> List[Dict]:
    """
    Получение вакансий по id компании
    """
    url = f"{HH_API_URL}/vacancies"
    params = {"employer_id": company_id, "per_page": 100}

    response = requests.get(url, params=params)

    if response.status_code != 200:

        return []

    vacancies = response.json().get("items", [])




    return vacancies
