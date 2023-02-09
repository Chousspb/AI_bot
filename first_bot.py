import logging
from os import environ
from dotenv import load_dotenv, find_dotenv
import telebot
import openai

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

load_dotenv(find_dotenv())
bot = telebot.TeleBot(environ["BOT_API_KEY"])
openai.api_key = environ["OPENAI_API_KEY"]
user_id = int(environ["USER_KEY"])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("👋 Привет!")
    btn2 = telebot.types.KeyboardButton("❓ Вопрос?")
    btn3 = telebot.types.KeyboardButton('СТОП')
    markup.add(btn1, btn2, btn3)
    if message.text == 'СТОП':
        bot.stop_bot()
    else:
        bot.send_message(chat_id=message.chat.id, text="Привет, я супер вумный бот! Можешь спросить у меня что хочешь", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def get_codex(message):
    if int(message.chat.id) != user_id:
        bot.send_message("Тебе нужен USER_KEY для использования бота")
    else:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt='"""\n{}\n"""'.format(message.text),
            temperature=0,
            max_tokens=1200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=['qqq']
        )

        bot.send_message(message.chat.id, f'\n{response["choices"][0]["text"]}\n')

bot.infinity_polling()
