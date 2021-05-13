import os
from itertools import count

import requests
from dotenv import load_dotenv
from terminaltables import SingleTable

PROGRAMMING_LANGUAGES = [
    "javascript", "Java", "C#",
    "Python", "Ruby", "Go",
    "PHP", "C++", "Swift"
]


def create_table(site_statistics, title):
    statistics_table = [(
        "Язык программирования",
        "Вакансий найдено",
        "Вакансий обработано",
        "Средняя зарплата"
    )]

    for language, statistics in site_statistics.items():
        language_statistics = [
            language,
            statistics["vacancies_found"],
            statistics["vacancies_processed"],
            statistics["average_salary"]
        ]
        statistics_table.append(language_statistics)
    table = SingleTable(statistics_table, title)
    return table


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_to:
        return salary_to * 0.8
    elif salary_from:
        return salary_from * 1.2


def add_statistic(vacancies, vacancies_processed, average_salary):
    statistic = {
        "vacancies_found": vacancies,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }

    return statistic


def get_sj_pages(secret_key, programming_language):
    vacancies_pages = []
    api_url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {"X-Api-App-Id": secret_key}
    number_vacancies_per_page = 10

    params = {
        "keywords[1][keys]": programming_language,
        "town": "Москва",
        "count": number_vacancies_per_page
    }

    for page in count():
        params["page"] = page

        response = requests.get(api_url, params, headers=headers)
        response.raise_for_status()
        response = response.json()

        vacancies_pages.append(response)
        if not response["more"]:
            return vacancies_pages


def get_hh_pages(programming_language):
    vacancies_pages = []
    api_url = "https://api.hh.ru/vacancies"

    moscow_area = 1
    period_days = 30

    params = {
        "text": programming_language,
        "area": moscow_area,
        "period": period_days,
    }

    for page in count():

        params["page"] = page
        response = requests.get(api_url, params)
        response.raise_for_status()
        response = response.json()
        last_page = response["pages"]-1
        vacancies_pages.append(response)

        if page == last_page:
            return vacancies_pages


def predict_rub_salary_sj(vacancies_pages):
    vacancies_processed = []

    for vacancies in vacancies_pages:
        for vacancy in vacancies["objects"]:

            if vacancy["currency"] != "rub":
                continue

            salary_from = vacancy["payment_from"]
            salary_to = vacancy["payment_to"]

            if not salary_from and not salary_to:
                continue

            average_salary = predict_salary(salary_from, salary_to)
            vacancies_processed.append(int(average_salary))
    average_salary = int(sum(vacancies_processed) / len(vacancies_processed))
    vacancies_processed = len(vacancies_processed)

    return average_salary, vacancies_processed


def predict_rub_salary_hh(vacancies_list):
    vacancies_processed = []
    for vacancies in vacancies_list:
        for vacancy in vacancies["items"]:
            if vacancy["salary"] is None:
                continue

            if vacancy["salary"]["currency"] != "RUR":
                continue

            salary_from = vacancy["salary"]["from"]
            salary_to = vacancy["salary"]["to"]
            average_salary = predict_salary(salary_from, salary_to)
            vacancies_processed.append(int(average_salary))

    average_salary = int(sum(vacancies_processed) / len(vacancies_processed))
    vacancies_processed = len(vacancies_processed)

    return average_salary, vacancies_processed


def get_hh_statistics():
    statistics = {}
    for programming_language in PROGRAMMING_LANGUAGES:

        vacancies_pages = get_hh_pages(programming_language)
        vacancies_found = vacancies_pages[0]["found"]
        average_salary, vacancies_processed = predict_rub_salary_hh(
            vacancies_pages)

        statistics[programming_language] = add_statistic(
            vacancies_found,
            vacancies_processed,
            average_salary
        )
    return statistics


def get_sj_statistics(secret_key):
    statistics = {}

    for programming_language in PROGRAMMING_LANGUAGES:
        vacancies_pages = get_sj_pages(
            secret_key, programming_language)

        average_salary, vacancies_processed = predict_rub_salary_sj(
            vacancies_pages)

        vacancies_found = vacancies_pages[0]["total"]

        statistics[programming_language] = add_statistic(
            vacancies_found,
            vacancies_processed,
            average_salary
        )
    return statistics


def main():
    load_dotenv()
    secret_key = os.getenv("SUPER_JOB_KEY")

    try:
        sj_statistics = get_sj_statistics(secret_key)
        hh_statistics = get_hh_statistics()
    except requests.exceptions.HTTPError as erorr:
        print(erorr)

    sj_table = create_table(sj_statistics, "SuperJob")
    hh_table = create_table(hh_statistics, "HeadHunter")
    print(sj_table.table)
    print(hh_table.table)


if __name__ == "__main__":
    main()
