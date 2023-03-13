import asyncio
import json
import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

load_dotenv()
API_TOKEN = os.environ.get('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class NewsState(StatesGroup):
    index = State()

def parse_news():
    """ Задаем URL-адреса для каждой категории новостей"""
    categories = {
        "Политика": "https://ria.ru/politics/",
        "Экономика": "https://ria.ru/economy/",
        "Общество": "https://ria.ru/society/",
        "Происшествия": "https://ria.ru/incidents/",
        "В мире": "https://ria.ru/world/"
    }

    """ Создаем словарь, который будет содержать новости для каждой категории"""
    news_dict = {"articles": {}}

    """ Проходимся по каждой категории и собираем новости"""
    for category, url in categories.items():
        # Получаем содержимое веб-страницы
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        """#Извлекаем заголовки, изображения и URL-адреса для каждой новости"""
        titles = [title.text.strip() for title in soup.find_all("a", {"class": "list-item__title"})]
        images = [image["src"] for image in soup.find_all("img", {"class": "responsive_img m-list-img"})]
        urls = [url["href"] for url in soup.find_all("a", {"class": "list-item__title"}, href=True)]

        """ Добавляем новости в словарь"""
        news_dict["articles"][category] = {"title": titles, "img": images, "url": urls}

    """ Сохраняем словарь в JSON"""
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news_dict, f, ensure_ascii=False, indent=4)


""" Загружаем данные из файла JSON"""
with open("news.json", "r", encoding="utf-8") as f:
    news_dict = json.load(f)

""" Функция для отправки пользователю списка новостей"""


async def send_news(chat_id: int, news_dict: dict, category: str, index: int) -> str:
    news = news_dict["articles"][category]
    message = f"<b>{category}:</b>\n\n"
    has_more_news = False

    for i in range(index, index + 5):
        if i >= len(news["title"]):
            has_more_news = False
            break

        title = news["title"][i]
        img = news["img"][i]
        url = news["url"][i]
        message += f"<b>❗{title}</b>\n<a href='{img}'>&#8205;</a>\n<a href='{url}'>Читать далее</a>\n\n"
        has_more_news = True

    if not has_more_news:
        message = "К сожалению, новости из этой категории закончились. Пожалуйста, вернитесь позже."

    return await bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")


def get_categories_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, input_field_placeholder='Выберите категорию...')
    categories = list(news_dict["articles"].keys())
    for i in range(0, len(categories), 3):
        row = categories[i:i+3]
        buttons = [KeyboardButton(text=category) for category in row]
        keyboard.add(*buttons)
    return keyboard



""" Обработчик команды /start"""
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message, state: FSMContext):
    keyboard = get_categories_keyboard()
    await message.answer("Привет! Я новостной бот. Выбери категорию новостей, которые ты хочешь получить:", reply_markup=keyboard)


    category = message.text
    await state.set_data({category: 0})

@dp.message_handler(lambda message: message.text in news_dict["articles"].keys())
async def process_category_command(message: types.Message, state: FSMContext):
    category = message.text
    chat_id = message.chat.id

    current_state = await state.get_data()
    current_index = current_state.get(category, 0)

    await send_news(chat_id, news_dict, category, current_index)
    await state.set_data({category: current_index + 5})


""" Запускаем бота"""
if __name__ == '__main__':
    parse_news()
    executor.start_polling(dp, skip_updates=True)
    async def periodic_task():
        while True:
            await parse_news()
            await asyncio.sleep(7200)

    asyncio.get_event_loop().create_task(periodic_task())
    asyncio.get_event_loop().run_forever()
