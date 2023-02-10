import logging
from os import environ
from dotenv import load_dotenv, find_dotenv
import telebot
import openai
from time import sleep

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

load_dotenv(find_dotenv())
bot = telebot.TeleBot(environ["BOT_API_KEY"])
openai.api_key = environ["OPENAI_API_KEY"]
user_id = environ["USER_KEY"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("/start")
    btn2 = telebot.types.KeyboardButton("👋 Привет!")
    btn3 = telebot.types.KeyboardButton('СТОП')
    markup.add(btn1, btn2, btn3)
    bot.send_message(chat_id=message.chat.id,
                     text="Привет, я супер вумный бот! Можешь спросить у меня что хочешь", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def get_codex(message):

    if message.text == 'СТОП':
        bot.send_message(chat_id=message.chat.id,
                     text="Всего хорошего! До встречи!")
        sleep(2)
        bot.stop_polling()
    else:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt='"""\n{}\n"""'.format(message.text),
            temperature=0,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0,
            stop=['СТОП']
        )

        bot.send_message(message.chat.id, f'\n{response["choices"][0]["text"]}\n')

bot.infinity_polling()
