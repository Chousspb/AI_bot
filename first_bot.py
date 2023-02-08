import logging
from os import environ as env
from dotenv import load_dotenv
import telebot
import openai

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

load_dotenv()
bot = telebot.TeleBot(env["BOT_API_KEY"])
openai.api_key = env["OPENAI_API_KEY"]
user_id = int(env["USER_KEY"])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id, text="Привет, я супер вумный бот! Можешь спросить у меня что хочешь")

@bot.message_handler(func=lambda message: True)
def get_codex(message):
    if int(message.chat.id) != user_id:
        bot.send_message("Тебе нужен USER_KEY для использования бота")
    else:
        response = openai.Completion.create(
            engine="text-davinci-003",
            # engine = "text-davinci-001",
            # engine = "text-curie-001",
            # engine = "text-babbage-001",
            # engine = "text-ada-001",
            # engine = "code-davinci-002",
            # engine = "code-cushman-001",
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
