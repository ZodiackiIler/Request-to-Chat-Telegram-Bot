# инициализируем необзходимые библиотеки
from aiogram import Dispatcher, types, executor
from aiogram.types import Message, ParseMode
from config import bot, dp, db, MESSAGE_LIMIT, INTERVAL_SECONDS, YOUR_ID, approve_message, video_message, photo_message, send_message
import asyncio
import datetime
import logging
from db import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

offset = datetime.timedelta(hours=3)
tz = datetime.timezone(offset, name='МСК')

######################################################
#
# Принятие в чат
#
######################################################

@dp.chat_join_request_handler()
async def chat_join_request(update: types.ChatJoinRequest):
    if not db.get_user_by_user_id(update.from_user.id):
        db.add_user(update.from_user.id)
        await bot.send_message(chat_id=update.from_user.id, text=approve_message, parse_mode=types.ParseMode.HTML)

        await asyncio.sleep(15)
        await update.approve()
    else:
        await bot.send_message(chat_id=update.from_user.id, text=approve_message, parse_mode=types.ParseMode.HTML)

        await asyncio.sleep(15)
        await update.approve()


@dp.message_handler(commands=['link_create'])
async def link_create(message: Message):
    if message.chat.type != 'private':
        if message.from_user.id == YOUR_ID:
            link = await bot.create_chat_invite_link(message.chat.id, creates_join_request=True)
            await bot.send_message(message.chat.id, f"Ссылка на вступление в чат: `{link.invite_link}`", parse_mode=types.ParseMode.MARKDOWN)
        else:
            print('Недостаточно прав')
            print(message.from_user.id), print(YOUR_ID)
    else:
        pass

####################################################
#
# Получение id
#
####################################################

@dp.message_handler(commands=['get_id'])
async def get_id(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    await bot.send_message(chat_id, f"Ваш ID: {user_id}\nChat ID: {chat_id}", parse_mode=types.ParseMode.HTML)

####################################################
#
# рассылка
#
####################################################

async def send_message_to_users():
    users = db.get_all_users()
    for user in users:
        try:
            await bot.send_message(user[1], send_message, parse_mode=types.ParseMode.HTML)
            await asyncio.sleep(1)  
        except Exception as e:
            print(f"Error sending message to user {user[1]}: {str(e)}")

@dp.message_handler(commands=['send_to_all'])
async def send_to_all(message):
    if message.from_user.id == YOUR_ID: 
        users_count = len(db.get_all_users())
        iterations = users_count // MESSAGE_LIMIT + 1
        for _ in range(iterations):
            await send_message_to_users()
            await asyncio.sleep(INTERVAL_SECONDS)
        await message.answer("Рассылка была завершена.")
    else:
        pass

@dp.message_handler(commands=['send_to_all_photo'])
async def send_photo_message_to_users(message):
    if message.from_user.id == YOUR_ID: 
        users = db.get_all_users()
        for user in users:
            try:
                with open("send/img.png", "rb") as photo_file:
                    await bot.send_photo(user[1], photo_file, caption=photo_message, parse_mode=types.ParseMode.HTML)
                await asyncio.sleep(1) 
            except Exception as e:
                print(f"Error sending photo to user {user[1]}: {str(e)}")
    else:
        pass

@dp.message_handler(commands=['send_to_all_video'])
async def send_video_message_to_users(message):
    if message.from_user.id == YOUR_ID: 
        users = db.get_all_users()
        for user in users:
            try:
                with open("send/video.mp4", "rb") as video_file:
                    await bot.send_video(user[1], video_file, caption=video_message, parse_mode=types.ParseMode.HTML)
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Error sending video to user {user[1]}: {str(e)}")
    else:
        pass


####################################################
#
# запуск бота
#
####################################################
async def on_startup(_):
    dt = datetime.datetime.now()
    tz.tzname(dt)
    print('Бот по заявкам вышел в онлайн')
    print(f'Время запуска: {dt}')

async def on_shutdown(dp):
    dt = datetime.datetime.now()
    tz.tzname(dt)
    print('Бот по заявкам вышел в оффлайн')
    print(f'Время отключения: {dt}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
