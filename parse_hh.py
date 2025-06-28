# parse_hh.py

import requests
from bs4 import BeautifulSoup

def get_text_from_hh(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Ошибка запроса: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Вакансия
    if "vacancy" in url:
        # Попробуем найти основной текст вакансии
        content_block = soup.find("div", {"data-qa": "vacancy-description"})
        if not content_block:
            content_block = soup.find("div", class_="g-user-content")  # fallback
    # Резюме
    elif "resume" in url:
        content_block = soup.find("div", {"data-qa": "resume-block-skills"})  # примерный блок
        if not content_block:
            content_block = soup.find("div", class_="resume-applicant-main")  # fallback
    else:
        raise Exception("Не удалось определить тип страницы (вакансия/резюме)")

    if not content_block:
        raise Exception("Не удалось найти текст на странице (возможно, структура изменилась)")

    return content_block.get_text(separator="\n", strip=True)

