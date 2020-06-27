import telebot
import config
import os
import logging
import util
import r2pygen as rgen
from flask import Flask, request


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start"])
def greet_user(msg: str):
    bot.send_message(msg.chat.id,
            ( 
                "Приветствую вас, благородный воин!\n"
                "Напиши /help, чтобы вывести список всех известных комманд.\n"
                "Напиши /train, чтобы порешать задачки."
            )
    )


@bot.message_handler(commands=["help"])
def helper(msg: str):
    bot.send_message(msg.chat.id, util.output_available_commands(util.command_dict))


@bot.message_handler(commands=["train"])
def get_tasks(msg: str):
    chat_id = msg.chat.id
    bot.send_message(chat_id, "Сколько задачек вам бы хотелось порешать?")
    bot.register_next_step_handler_by_chat_id(chat_id, generate_task_pdf)


def generate_task_pdf(msg: str):
    chat_id = msg.chat.id
    try:
        num = int(msg.text)
        if num > 40:
            bot.send_message(chat_id, "Выберите число поменьше (<= 40)")
            bot.register_next_step_handler_by_chat_id(chat_id, generate_task_pdf)
        elif num <= 0:
            bot.send_message(chat_id, "Выберите число побольше (>= 1)")
            bot.register_next_step_handler_by_chat_id(chat_id, generate_task_pdf)
        else:
            questions = rgen.rxm.get_questions(config.path2src)
            res = rgen.rxm.generate(questions, n_problems=num)
            file_name = util.strVec2str(res[0])
            with open(f"R/pdf/{file_name}1.pdf", "rb") as f:
                bot.send_document(chat_id, f, caption="Don't Panic!")
            os.remove(f"R/pdf/{file_name}1.pdf")
    except(ValueError):
        bot.send_message(chat_id, "Пожалуйста, используйте целочисленный ввод")
        bot.register_next_step_handler_by_chat_id(chat_id, generate_task_pdf)


server = Flask(__name__)


@server.route(f"/{config.token}", methods=["POST"])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{config.heroku_app_url}.com/{config.token}")
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
