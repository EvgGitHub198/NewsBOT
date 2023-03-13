import requests
from bs4 import BeautifulSoup
import json

"""Задаем URL-адреса для каждой категории новостей"""
categories = {
    "Политика": "https://ria.ru/politics/",
    "Экономика": "https://ria.ru/economy/",
    "Общество": "https://ria.ru/society/",
    "Происшествия": "https://ria.ru/incidents/",
    "В мире": "https://ria.ru/world/"
}

"""Создаем словарь, который будет содержать новости для каждой категории"""
news_dict = {"articles": {}}

""" Проходимся по каждой категории и собираем новости"""
for category, url in categories.items():
    """Получаем содержимое веб-страницы"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    """Извлекаем заголовки, изображения и URL-адреса для каждой новости"""
    titles = [title.text.strip() for title in soup.find_all("a", {"class": "list-item__title"})]
    images = [image["src"] for image in soup.find_all("img", {"class": "responsive_img m-list-img"})]
    urls = [url["href"] for url in soup.find_all("a", {"class": "list-item__title"}, href=True)]

    """Добавляем новости в словарь"""
    news_dict["articles"][category] = {"title": titles, "img": images, "url": urls}

""" Сохраняем словарь в JSON"""
with open("news.json", "w", encoding="utf-8") as f:
    json.dump(news_dict, f, ensure_ascii=False, indent=4)
