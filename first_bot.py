import logging
from os import environ
from dotenv import load_dotenv, find_dotenv
import telebot
import openai
from time import sleep
import random
import os

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

load_dotenv(find_dotenv())
bot = telebot.TeleBot(environ["BOT_API_KEY"])
openai.api_key = environ["OPENAI_API_KEY"]
user_id = environ["USER_KEY"]



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("/start")
    btn2 = telebot.types.KeyboardButton("Пришли мем")
    btn3 = telebot.types.KeyboardButton('СТОП')
    markup.add(btn1, btn2, btn3)
    bot.send_message(chat_id=message.chat.id,
                     text="Привет, я супер вумный бот! Можешь спросить у меня что хочешь", reply_markup=markup)

conversations = {}
@bot.message_handler(func=lambda message: True)
def get_codex(message):
    user_id = message.from_user.id
    sent_photo = False
    if user_id not in conversations:
        conversations[user_id] = []
    conversation = conversations[user_id]

    if message.text == 'Пришли мем':
        img_list = os.listdir(r'/Users/Admin/dom_u_morya/sites/bot/photo/')
        img_path = random.choice(img_list)
        bot.send_photo(chat_id=message.chat.id, photo=open('/Users/Admin/dom_u_morya/sites/bot/photo/' + img_path, 'rb'))
        sent_photo = True
    elif message.text == 'СТОП':
        bot.send_message(chat_id=message.chat.id,
                     text="Всего хорошего! До встречи!")
        sleep(2)
        bot.stop_polling()
    else:
        conversation.append(message.text)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt='"""\n{}\n"""'.format("\n".join(conversation)),
            temperature=0.2,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0,
            stop=['СТОП']
        )
        bot.send_message(message.chat.id, f'\n{response["choices"][0]["text"]}\n')
        conversation.append(response["choices"][0]["text"])


bot.infinity_polling()
