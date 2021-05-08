import os

import requests
from dotenv import load_dotenv
from terminaltables import SingleTable

PROGRAMMING_LANGUAGES = [
    "Golang", "Java", "C#",
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
    pages_number = 10
    number_vacancies_per_page = 10

    for page in range(pages_number):
        params = {
            "keywords[1][keys]": programming_language,
            "town": "Москва",
            "page": page,
            "count": number_vacancies_per_page 
        }
        vacancies_pages.append(requests.get(
            api_url, params, headers=headers).json())
    return vacancies_pages


def get_hh_pages(programming_language):
    vacancies_pages = []
    api_url = "https://api.hh.ru/vacancies"

    moscow_area = 1
    period_days = 30
    pages_number = 100

    for page in range(pages_number):
        params = {
            "text": programming_language,
            "area": moscow_area,
            "period": period_days,
            "page": page
        }

        vacancies_pages.append(requests.get(api_url, params).json())
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


def get_hh_statistics(programming_language, hh_statistics):

    vacancies_hh_pages = get_hh_pages(programming_language)
    vacancies_hh_found = vacancies_hh_pages[0]["found"]
    average_hh_salary, vacancies_hh_processed = predict_rub_salary_hh(
        vacancies_hh_pages)

    hh_statistics[programming_language] = add_statistic(
        vacancies_hh_found,
        vacancies_hh_processed,
        average_hh_salary
    )
    return hh_statistics


def get_sj_statistics(programming_language, sj_statistics, secret_key):

    vacancies_sj_pages = get_sj_pages(
        secret_key, programming_language)

    average_sj_salary, vacancies_sj_processed = predict_rub_salary_sj(
        vacancies_sj_pages)

    vacancies_sj_found = vacancies_sj_pages[0]["total"]

    sj_statistics[programming_language] = add_statistic(
        vacancies_sj_found,
        vacancies_sj_processed,
        average_sj_salary
    )
    return sj_statistics


def main():
    load_dotenv()
    secret_key = os.getenv("SUPER_JOB_KEY")
    sj_statistics = {}
    hh_statistics = {}
    for programming_language in PROGRAMMING_LANGUAGES:
        sj_statistics = get_sj_statistics(
            programming_language, sj_statistics, secret_key)

        hh_statistics = get_hh_statistics(programming_language, hh_statistics)

    sj_table = create_table(sj_statistics, "SuperJob")
    hh_table = create_table(hh_statistics, "HeadHunter")
    print(sj_table.table)
    print(hh_table.table)


if __name__ == "__main__":
    main()
