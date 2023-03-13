# import asyncio
# import os
# import requests
# from aiogram import Bot, Dispatcher, types
# from aiogram.types import ParseMode
# from dotenv import load_dotenv
#
# load_dotenv()
#
# API_TOKEN = os.environ.get('BOT_TOKEN')
# NEWS_API_KEY = os.environ.get('NEWS_API')
#
# bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
# dp = Dispatcher(bot)
#
# # Словарь для хранения текущих номеров пятерок для каждой категории
# current_news_numbers = {
#     "general": 0,
#     "sports": 0,
#     "health": 0,
#     "entertainment": 0,
#     "technology": 0,
# }
#
# def start_message():
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     itembtn1 = types.KeyboardButton('Общие')
#     itembtn2 = types.KeyboardButton('Спорт')
#     itembtn3 = types.KeyboardButton('Здравоохранение')
#     itembtn4 = types.KeyboardButton('Развлечения')
#     itembtn5 = types.KeyboardButton('Технологии')
#     markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
#
#     return 'Привет! Я новостной бот. Выбери тему новостей, которые ты хочешь получить.', markup
#
#
# def get_news(category):
#     current_number = current_news_numbers[category]
#     response = requests.get(f"https://newsapi.org/v2/top-headlines?country=ru&category={category}&apiKey={NEWS_API_KEY}")
#     news = response.json()["articles"]
#     result = []
#     for article in news[current_number:current_number+5]:
#         title = article['title']
#         if article['description'] != 'None':
#             description = article['description']
#         else:
#             description = article.get('content', 'Нет описания')
#         url = article['url']
#         result.append(f"🔹<b>{title}</b>\n\n<a href='{url}'>Читать далее</a>\n\n")
#     current_news_numbers[category] += 5
#     return "\n".join(result)
#
#
# @dp.message_handler(commands=['start'])
# async def send_welcome(message: types.Message):
#     start_msg, markup = start_message()
#     await message.answer(start_msg, reply_markup=markup)
#
# last_news_index = {}
# @dp.message_handler(content_types=types.ContentTypes.TEXT)
# async def send_news(message: types.Message):
#     if message.text == 'Общие':
#         category = "general"
#     elif message.text == 'Спорт':
#         category = "sports"
#     elif message.text == 'Здравоохранение':
#         category = "health"
#     elif message.text == 'Развлечения':
#         category = "entertainment"
#     elif message.text == 'Технологии':
#         category = "technology"
#     else:
#         await message.answer("Неизвестная команда")
#         return
#
#     news = get_news(category)
#
#     if not news:
#         await message.answer("Больше новостей нет.")
#         return
#
#     await message.answer(f"<b>{message.text}:</b>\n\n{news}", parse_mode=ParseMode.HTML)
#     current_news_numbers[category] += 5
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(dp.start_polling())
