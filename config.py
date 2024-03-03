# инициализируем необзходимые библиотеки
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import os
from dotenv import main
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import DBHelper

storage=MemoryStorage()

main.load_dotenv()

TOKEN_BOT = os.getenv('TOKEN_BOT')
YOUR_ID=YOUR_TELEGRAM_ID

approve_message="текст сообщения бота в лс пользователю при приеме заявки"
video_message="Ваше сообщение рассылки здесь"
photo_message="Ваше сообщение рассылки здесь"
send_message="Ваше сообщение рассылки здесь"

MESSAGE_LIMIT = 5
INTERVAL_SECONDS = 60

# Объект бота
bot = Bot(TOKEN_BOT);
# Диспетчер
dp = Dispatcher(bot, storage=storage)
db = DBHelper('users.db')
